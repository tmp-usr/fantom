import os
import csv


from fantom.src.sqling.project_orm import MetadataORM, MetadataValueORM, SampleMetadataORM, SampleORM, ProjectORM


from storm.locals import *
from biom import load_table

from project_selector import ProjectSelector

from pandas import read_csv

import pdb
class ProjectUpdater(object):
    
    def __init__(self, project_name, store, metadata_file):
        
        self.store=store
        self.project_name=project_name

        self.header=[]
        self.Fields={}
        
        project= self.store.find(ProjectORM, ProjectORM.name == unicode(self.project_name)).one()
        
        #new project
        if project is None:

            self.metadata_file=metadata_file
            self.project=self.create_project(self.project_name) 
            self.project_selector= ProjectSelector(project_name, store)
            
            if self.project: 
                self.read_metadata(self.metadata_file) 
                self.insert_metadata_value()
                #self.insert_sample_metadata(self.metadata_file)
                self.store.flush()
            else:
                raise Exception
        
        #update project
        else:
            self.project= project
            self.project_selector= ProjectSelector(project_name, store)
            
            self.metadata_file= metadata_file
            self.project.metadata_path = unicode(self.metadata_file)
            
            self.read_metadata(self.metadata_file)
            self.insert_metadata_value()
            #self.insert_sample_metadata(self.metadata_file)
            self.store.flush()



    def create_project(self, project_name):       
        project=ProjectORM()
        project.name=unicode(project_name)
        project.metadata_path = unicode(self.metadata_file)
        if os.path.exists(project.metadata_path):
            self.store.add(project)
            self.store.commit()
            return project
        else:
            return None


    def read_metadata(self,metadata_file):
        
        with open(metadata_file,"rb") as metadata_input:
            dialect = csv.Sniffer().sniff(metadata_input.read(1024))
            
        self.df_metadata= read_csv(metadata_file, sep= dialect.delimiter, dtype={'Sample': str})
        self.df_metadata= self.df_metadata.set_index("Sample")
        

    def insert_metadata_value(self):
        #ids should be unique!!
        #lastInsert_id=self.store.execute('SELECT MAX(id) FROM metadata').get_one()[0]
        
        field_names= self.df_metadata.columns
        
        for field_name in field_names:
            md= self.store.find(MetadataORM, (MetadataORM.name == unicode(field_name)) & 
                    (MetadataORM.project_id == self.project.id)).one()

            if not md:
                md= MetadataORM()
                md.name = unicode(field_name) 
                md.project_id = self.project.id
                data_type= self.df_metadata[field_name].dtype
                
                if data_type == str or data_type == object:
                    md.data_type=1               
                     
                elif data_type == int:
                    md.data_type=2               
                    
                elif data_type == float:
                    md.data_type=3               

                self.store.add(md)
        
        for index in self.df_metadata.index:
            ### inserting into the sample table
            sample= self.store.find(SampleORM, (SampleORM.name == unicode(index)) & 
                    (SampleORM.project_id == self.project.id)).one()
            
            if not sample:
                sample= SampleORM()
                sample.name= unicode(index)
                sample.project= self.project
                self.store.add(sample)  
            
            for field_name in field_names:
                md= self.store.find(MetadataORM, (MetadataORM.name == unicode(field_name)) & 
                        (MetadataORM.project_id == self.project.id)).one()
                
                v= self.df_metadata[field_name][index]
                if md.data_type == 1:
                    mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) &
                            MetadataValueORM.string_value == unicode(v)).one()
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id
                    
                    mv.string_value= unicode(v)
                
                elif md.data_type == 2:
                    mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) &
                            MetadataValueORM.int_value == int(v)).one()
                    
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id

                    
                    mv.int_value= int(v)

                elif md.data_type == 3:
                    try:
                        mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) &
                            MetadataValueORM.float_value == float(v)).one()
                    except:

                        mvs = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) &
                            MetadataValueORM.float_value == float(v))
                        pdb.set_trace()
                        
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id

                    
                    mv.float_value= float(v)
                
                self.store.add(mv)


                sm=  self.store.find(SampleMetadataORM, (SampleMetadataORM.sample_id == sample.id) &
                        (SampleMetadataORM.metadata_value_id == mv.id)).one()

                if not sm:
                    sm= SampleMetadataORM()
                    sm.sample_id = sample.id
                    sm.metadata_value_id= mv.id

                self.store.add(sm)

        self.store.commit()


    def metadata_from_biom(self, biom_table_path, project_name, store):
        biom_table= load_table(biom_table_path)
        sample_metadata= biom_table.metadata(axis= 'sample')
        obs_metadata= biom_table.metadata(axis= 'observation')
        sample_ids= biom_table.ids(axis= 'sample')
        obs_ids= biom_table.ids(axis= 'observation')
        p= Project(project_name)
        for i in range(len(sample_metadata)):
            metadata= sample_metadata[i]
            sample_id= sample_ids[i]
            Metadata= {}
            for k,v in metadata.iteritems():
                Metadata[k]=v
            s= SampleORM(sample_id, Metadata)
            p.update({s.name: s})
        p.to_tsv()
        ### TO BE CONTINUED!!!

        #md= MetadataAdapter(p.name, store, p.tsv)

