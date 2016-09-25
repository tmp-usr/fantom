import os
import errno

#import csv
from fantom.sqling.project_orm import MetadataORM, MetadataValueORM, SampleMetadataORM, SampleORM, ProjectORM


from storm.locals import *
from biom import load_table

from project_selector import ProjectSelector

from pandas import read_csv

import pdb



class ProjectUpdater(ProjectBase):
    def __init__(self, project_name, store):
        ProjectBase.__init__(self, project_name, store)
        
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


class ProjectSelector(ProjectBase):
    def __init__(self, project_name, store):
        ProjectBase.__init__(self, project_name, store)

    
    
    def get_all_metadata(self, categorical=False):
        samples= self.store.find(SampleORM, SampleORM.project_id == self.project_orm.id )
        
        for sample in samples:
            sm= self.store.find(SampleMetadataORM, SampleMetadataORM.sample_id == sample.id)
            for sample_metadata in sm:
                mv= self.store.find(MetadataValueORM, MetadataValueORM.id == sample_metadata.metadata_value_id)
                for metadata_value in mv:
                    metadata= self.store.find(MetadataORM, MetadataORM.id == metadata_value.metadata_id).one()
                    
                    if categorical:
                        if not metadata.data_type == 1:
                            continue
                        value= metadata_value.string_value
                        print metadata.name, value, sample.name

                    else:
                        if not metadata.data_type == 1:
                            value= metadata_value.string_value
                    
                        elif metadata.data_type == 2:
                            value= metadata_value.int_value
                
                        elif metadata.data_type == 3:
                            value= metadata_value.float_value

                        print metadata.name, value, sample.name

    
    
    def get_metadata_names(self):
        return [metadata.name for metadata in 
                self.store.find(MetadataORM, MetadataORM.project_id == 
                self.project_orm.id)]

    
    #def convert_type(self, metadata):
    #    if self.get_metadata()[metadata.metadata.name] == 1:
    #        return metadata

    #    elif self.get_metadata()[metadata.metadata.name] == 2:
    #        setattr(metadata,value,Int())
    #        return metadata
    #    else:
    #        setattr(metadata,value,Float())
    #        return metadata




    def build_expression(self, MetadataORM, MetadataValueORM, prop, value, operator):
        meta=self.store.find(MetadataORM, MetadataORM.name == unicode(prop)).one()
        
        if meta.data_type==1:        
            my_value = MetadataValueORM.string_value
            value= unicode(value)

        elif meta.data_type==2:    
            my_value = MetadataValueORM.int_value
            value= int(value)    

        elif meta.data_type==3:        
            my_value =  MetadataValueORM.float_value
            value= float(value)

        
        if operator == 'contains':
            return (my_value.like('%'+ value+ '%')) 

        elif operator == '=':
            return (my_value == value)
        
        elif operator == '<':
            return (my_value < value)

        elif operator == '>':
            return (my_value > value)

        elif operator == '<=':
            return (my_value <= value)

        elif operator == '>=':
            return (my_value >= value)
    
    
    #def get_all_samples(self):        
        #SampleORM.metadata = ReferenceSet(SampleORM.id,
        #        SampleMetadataORM.sample_id, 
        #        SampleMetadataORM.metadata_value_id,
        #        MetadataValueORM.id)
        
        #return [sample for sample in self.store.find(SampleORM, 
        #    SampleORM.project_id == self.project_orm.id)]



    def get_samples_by_category(self):
        """
            returns a dict with the keys as categories and values as samples.
        """
        category_types= self.get_categorical_metadata()
        CategoryType= {}
        for category_type in category_types:
            categories= self.get_prop_values(category_type)
            if category_type not in CategoryType:
                CategoryType[category_type]= {}
            for category in categories: 
                if category not in CategoryType[category_type]:
                    CategoryType[category_type][category]=[]
                CategoryType[category_type][category]= [sample.name for sample in self.get_samples_by_prop(category_type, category, '=' )] 
        return CategoryType 
        



    #def get_prop_values(self, prop):
    #    return list(set([[[str(value) for value in (metadata.string_value,metadata.int_value,metadata.float_value) if value is not None ][0] for metadata in sample.metadata if metadata.metadata.name == unicode(prop)][0] for sample in self.get_all_samples()]))


    
    def get_metadata_by_sample_name(self, sample_name):
        
        SampleORM.metadata = ReferenceSet(SampleORM.id,
            SampleMetadataORM.sample_id,SampleMetadataORM.metadata_value_id,
            MetadataValueORM.id)
        
        def not_none(a):
            if a is not None: 
                if a==0:
                    return str(a)
                else:
                    return a
        
        MD={}
        try:
            for metadata in self.store.find(MetadataValueORM, 
                SampleMetadataORM.sample_id == SampleORM.id,
                SampleMetadataORM.metadata_value_id == MetadataValueORM.id,
                MetadataValueORM.metadata_id==MetadataORM.id, 
                (SampleORM.name == sample_name)):
                
                MD[metadata.metadata.name] = filter(not_none,
                            (metadata.string_value, metadata.int_value, 
                                metadata.float_value))[0]
            
        except:
            print metadata.metadata.name, (metadata.string_value, 
                    metadata.int_value, metadata.float_value)
            print sample_name
                                         
        return MD 
            
    
    #def get_sample_metadata_by_name(self, sample_name, metadata_name):        
    #    return self.store.find(SampleMetadataORM, 
    #        SampleMetadataORM.sample_id == SampleORM.id,
    #        SampleMetadataORM.metadata_value_id == MetadataValueORM.id,
    #        MetadataValueORM.metadata_id==MetadataORM.id, 
    #        (SampleORM.name == unicode(sample_name)) & 
    #        (MetadataORM.name == unicode(metadata_name))).one()
    

    def get_categorical_metadata(self):
        return [ metadata for metadata,data_type in
                self.get_metadata().iteritems() if data_type == 1]



    def get_samples_by_metadata(self, metadata_name, metadata_value, operator):
        
        SampleORM.metadata = ReferenceSet(SampleORM.id,
                SampleMetadataORM.sample_id,SampleMetadataORM.metadata_value_id,
                MetadataValueORM.id)
        
        return [sample for sample in self.store.find(SampleORM, 
            SampleMetadataORM.sample_id == SampleORM.id,
            SampleMetadataORM.metadata_value_id == MetadataValueORM.id,
            MetadataValueORM.metadata_id==MetadataORM.id, 
            (MetadataORM.name == unicode(prop)) & 
            self.build_expression(MetadataORM,
                MetadataValueORM,prop,value,operator))]


class ProjectInserter(ProjectBase):
    
    def __init__(self, project_name, store, metadata_file= ""):
        
        ProjectBase.__init__(self, project_name, store)

        self.header=[]
        self.Fields={}
        
        #self.delete_metadata(project.name)

        #new project
        if not self.exists:

            if metadata_file == "":
                raise Exception("metadata_file argument cannot be blank!")

            self.metadata_file=metadata_file
            self.project_orm=self.create_project(self.project_name) 
            
            self.read_metadata(self.metadata_file) 
            self.insert_metadata_value()
            self.store.flush()
        
        else:
            print "Use the ProjectUpdater class."


    def create_project(self, project_name):       
        project=ProjectORM()
        project.name= project_name
        
        if os.path.exists(self.metadata_file):
            self.store.add(project)
            self.store.commit()
            return project
        else:
            raise FileNotFoundError(errno.ENOENT, 
                    os.strerror(errno.ENOENT), self.metadata_file)


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
                    (SampleORM.project_id == self.project_orm.id)).one()
            
            if not sample:
                sample= SampleORM()
                sample.name= index
                sample.project= self.project_orm
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

