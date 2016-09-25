import os
#import csv


from fantom.sqling.project_orm import MetadataORM, MetadataValueORM, SampleMetadataORM, SampleORM, ProjectORM


from storm.locals import *
from biom import load_table

from project_selector import ProjectSelector

from pandas import read_csv

import pdb
class ProjectUpdater(object):
    
    def __init__(self, project_name, store, metadata_file= ""):
        
        self.store=store
        self.project_name= unicode(project_name)

        self.header=[]
        self.Fields={}
        
        project= self.store.find(ProjectORM, ProjectORM.name == self.project_name).one()
        
        #self.delete_project_data(project.name)

        #new project
        if project is None:

            if metadata_file == "":
                raise Exception("metadata_file argument cannot be blank!")

            self.metadata_file=metadata_file
            self.project=self.create_project(self.project_name) 
            self.project_selector= ProjectSelector(self.project_name, store)
            if self.project: 
                self.read_metadata(self.metadata_file) 
                self.insert_metadata_value()
                #self.insert_sample_metadata(self.metadata_file)
                self.store.flush()
            else:
                raise Exception
        
        #update project
        #else:
        #    self.project= project
        #    self.project_selector= ProjectSelector(project_name, store)
        #    
        #    self.metadata_file= metadata_file
        #    self.project.metadata_path = unicode(self.metadata_file)
        #    
        #    self.read_metadata(self.metadata_file)
        #    self.insert_metadata_value()
        #    #self.insert_sample_metadata(self.metadata_file)
        #    self.store.flush()



    def create_project(self, project_name):       
        project=ProjectORM()
        project.name= project_name
        project.metadata_path = unicode(self.metadata_file)
        if os.path.exists(project.metadata_path):
            self.store.add(project)
            self.store.commit()
            return project
        else:
            return None



    def delete_project_data(self, project_name):
        project= self.store.find(ProjectORM, ProjectORM.name == unicode(project_name)).one()
        samples= self.store.find(SampleORM, SampleORM.project_id == project.id)

        for sample in samples:
            sample_metadatas= self.store.find(SampleMetadataORM, SampleMetadataORM.sample_id == sample.id)
            for sample_metadata in sample_metadatas:
                metadata_value= self.store.find(MetadataValueORM, MetadataValueORM.id == sample_metadata.metadata_value_id).one()
                if metadata_value:
                    self.store.remove(metadata_value)
                    self.store.remove(sample_metadata)
            
            self.store.remove(sample)
        self.store.remove(project)
        self.store.commit()



    def read_metadata(self,metadata_file):
        
        index_column= ""
        with open(metadata_file,"rb") as metadata_input:
            header= metadata_input.read(1024).split('\n')[0]
            index_column= header.split("\t")[0]
        
        self.df_metadata= read_csv(metadata_file, sep= "\t", dtype={index_column: str})
        self.df_metadata= self.df_metadata.set_index(index_column)
        

    def insert_metadata_value(self):
        #ids should be unique!!
        #lastInsert_id=self.store.execute('SELECT MAX(id) FROM metadata').get_one()[0]
        
        self.df_metadata.columns= map(unicode, map(str.strip, self.df_metadata.columns))
        self.df_metadata.index= map(unicode, map(str.strip, self.df_metadata.index))

        field_names= self.df_metadata.columns
        index_names= self.df_metadata.index

        for field_name in field_names:
            
            md= self.store.find(MetadataORM, (MetadataORM.name.lower() == field_name.lower())).one()

            if not md:
                md= MetadataORM()
                md.name = field_name
                self.store.add(md)

            data_type= self.df_metadata[field_name].dtype
            if data_type == str or data_type == object:
                md.data_type=1               
                 
            elif data_type == int:
                md.data_type=2               
                
            elif data_type == float:
                md.data_type=3               
            
            self.store.commit()
                        
        for index in self.df_metadata.index:
            ### inserting into the sample table
            sample= self.store.find(SampleORM, (SampleORM.name == index) & 
                    (SampleORM.project_id == self.project.id)).one()
            
            if not sample:
                sample= SampleORM()
                sample.name= index
                sample.project= self.project
                self.store.add(sample)  
                self.store.commit()
            

            for field_name in field_names:
                md= self.store.find(MetadataORM, (MetadataORM.name.lower() == field_name.lower()) ).one()
                
                v= self.df_metadata[field_name][index]

                if md.data_type == 1:
                    v= unicode(v.strip())
                    mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) & (MetadataValueORM.string_value == v)).one()
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id
                        mv.string_value= v
                        self.store.add(mv)
                
                elif md.data_type == 2:
                    mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) & (MetadataValueORM.int_value == int(v))).one()
                    
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id
                        mv.int_value= int(v)
                        self.store.add(mv)
                
                elif md.data_type == 3:
                    mv = self.store.find(MetadataValueORM, (MetadataValueORM.metadata_id == md.id) & (MetadataValueORM.float_value == float(v))).one()
                        
                    if not mv:
                        mv = MetadataValueORM()
                        mv.metadata_id = md.id 
                        mv.float_value= float(v)
                        self.store.add(mv)
                
                self.store.commit()

                sm=  self.store.find(SampleMetadataORM, (SampleMetadataORM.sample_id == sample.id) & (SampleMetadataORM.metadata_value_id == mv.id)).one()

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





fantomii_db= "../project/fantomii.db"

input_dir= "/Users/kemal/Desktop/postdoc/projects/low_carb/fantom_inputs/"
metadata_file_path= os.path.join(input_dir, "low_carb_metadata.tsv")

fantom_sqlite_db = create_database("sqlite:%s" % fantomii_db )
store= Store(fantom_sqlite_db)

pu= ProjectUpdater("a", store, metadata_file_path)

