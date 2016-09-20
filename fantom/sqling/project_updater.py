import os

from fantom.src.sqling.project_orm import MetadataORM, MetadataValueORM, SampleMetadataORM, SampleORM, ProjectORM


from storm.locals import *
from biom import load_table

from project_selector import ProjectSelector




NOTE = """

CURRENTLY SUSPENDED THE UPDATE MODULE!
WE CAN ONLY INSERT NEW METADATA BUT CANNOT
UPDATE THE EXSTNG in the SQLTE DATABASE
"""


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
            if self.project: 
                self.read_metadata(self.metadata_file) 
                self.insert_metadata_value()
                self.insert_sample_metadata(self.metadata_file)
                self.store.flush()
            else:
                raise Exception
        
        #update project
        else:
            error_message= """There is a problem with the update module. FIX IT LATER!!!
            """
            
            print error_message
            #self.project= project
            
            #self.metadata_file= metadata_file
            #self.project.metadata_path = unicode(self.metadata_file)
            
            #self.read_metadata(self.metadata_file)
            #self.update_metadata_value()
            #self.insert_sample_metadata(self.metadata_file)
            #self.store.flush()


        self.project_selector= ProjectSelector(project_name, store)
    
    
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
        with open(metadata_file) as fMeta:
            self.header=fMeta.readline().rstrip().split('\t')
            for line in fMeta:
                # first column should always be the name column and it should be of data type string
                columns = line.rstrip().split('\t')
                for k,v in enumerate(columns):
                    if k not in self.Fields:
                        self.Fields[k]=[]
                    self.Fields[k].append(v)

        for k,v in self.Fields.iteritems():
            for i in range(len(v)):
                try:
                    self.Fields[k][i]=int(self.Fields[k][i])
                except:
                    try:
                        self.Fields[k][i]=float(self.Fields[k][i])
                    except:
                        pass

 
    def update_metadata_value(self):
        lastInsert_id=self.store.execute('SELECT MAX(id) FROM metadata').get_one()[0]
        
        for k,v in self.Fields.iteritems():
            
            if k == 0:
                samples= list(set([i for i in v]))
                for s in samples:
                    sample= self.store.find(SampleORM,SampleORM.name == unicode(s)).one()
                    if sample is None:
                        sample=SampleORM()
                        sample.name=unicode(s)
                        sample.project_id=self.project.id
                        self.store.add(sample)
            else:
                meta = self.store.find(MetadataORM, MetadataORM.name == unicode(self.header[k])).one()
                values= list(set([unicode(i) for i in v]))
                
                if meta is None:
                    meta=MetadataORM()
                    new_id=k
                    if lastInsert_id is not None:
                        new_id=lastInsert_id+k
                    
                    meta.id= new_id
                    meta.name= unicode(self.header[k])
                    meta.project_id= self.project.id 
                    
                    types= list(set([type(i) for i in list(v)]))

                    if len(types) == 1:
                        if types[0] == str: meta.data_type=1               
                        elif types[0] == int: meta.data_type=2               
                        elif types[0] == float: meta.data_type=3               
                    
                    else:
                        if str in types and float in types or str in types and int in types:
                            meta.data_type=1 
                        elif float in types and int in types: 
                            meta.data_type=3 
                    
                    self.store.add(meta)
               

                for v in values:

                    if meta.data_type == 1:
                       
                        if mv is None:
                            mv=MetadataValueORM()
                            mv.metadata_id=meta.id
                            mv.string_value=v
                            self.store.add(mv)
                        
                        else:
                            mv.string_value= v

                    elif meta.data_type == 2:
                        mv=self.store.find(MetadataValueORM, 
                                (MetadataValueORM.metadata_id == meta.id) & 
                                (MetadataValueORM.int_value == int(v))).one()
                        
                        if mv is None:
                            mv=MetadataValueORM()
                            mv.metadata_id=meta.id
                            mv.int_value= int(v)
                            self.store.add(mv)
                        else:
                            mv.int_value= int(v)

                    elif meta.data_type == 3:
                        mv=self.store.find(MetadataValueORM, 
                                (MetadataValueORM.metadata_id == meta.id)).one()
                        
                        if mv is None:
                            mv=MetadataValueORM()
                            mv.metadata_id=meta.id
                            mv.float_value= float(v)
                            self.store.add(mv)
                        else:
                            mv.float_value= float(v)
                
                #self.store.commit()    
                
                #sm= self.project_selector.query_sample_metadata_by_name(sample.name, meta.name)
                #sm.remove()

                #self.store.commit()
                #new_sm= SampleMetadataORM()
                #new_sm.sample_id= sample.id
                #new_sm.metadata_value_id= mv.id
       
            self.store.commit()

    def insert_metadata_value(self):
        #ids should be unique!!
        lastInsert_id=self.store.execute('SELECT MAX(id) FROM metadata').get_one()[0]
        for k,v in self.Fields.iteritems():
            if k==0:
                samples= list(set([i for i in v]))
                for s in samples:
                    sample=SampleORM()
                    sample.name=unicode(s)
                    sample.project=self.project
                    self.store.add(sample)
            else:
                meta=MetadataORM()
                new_id=k
                if lastInsert_id is not None:
                    new_id=lastInsert_id+k
                
                meta.id=new_id
                meta.name=unicode(self.header[k])
                meta.project_id=self.project.id
                types= list(set([type(i) for i in v]))
                values= list(set([unicode(v) for v in v]))
                if len(types) == 1:
                    if types[0] == str:
                        meta.data_type=1               
                         
                    elif types[0] == int:
                        meta.data_type=2               
                        
                    
                    elif types[0] == float:
                        meta.data_type=3               
                
                else:
                    
                    if str in types and float in types or str in types and int in types:
                        meta.data_type=1 

                    
                    elif float in types and int in types:
                        meta.data_type=3 
                
                self.store.add(meta)
                self.store.commit()

                for v in values:
                    mv=MetadataValueORM()
                    mv.metadata_id=new_id
                    if meta.data_type == 1:
                        mv.string_value=v
                    elif meta.data_type == 2:
                        mv.int_value=int(v)
                    elif meta.data_type == 3:
                        mv.float_value=float(v)
                    
                    self.store.add(mv)

            self.store.commit()


    def insert_sample_metadata(self, metadata_file):
        with open(metadata_file) as fMeta:
            
            SampleORM.metadata = ReferenceSet(SampleORM.id,
                    SampleMetadataORM.sample_id,SampleMetadataORM.metadata_value_id,
                    MetadataValueORM.id)
            
            fMeta.readline()
            for line in fMeta:
                columns = line.rstrip().split('\t')
                sample=self.store.find(SampleORM,SampleORM.name == unicode(columns[0])).one()
                for i in range(1,len(columns)):
                    meta=self.store.find(MetadataORM, 
                            MetadataORM.name == unicode(self.header[i])).one()
                    if meta.data_type == 1:
                        mv=self.store.find(MetadataValueORM, 
                            MetadataValueORM.metadata_id == MetadataORM.id, 
                            (MetadataORM.name == unicode(self.header[i])) & 
                            (MetadataValueORM.string_value == unicode(columns[i]))).one()
                    
                    elif meta.data_type == 2:
                        mv=self.store.find(MetadataValueORM, 
                            MetadataValueORM.metadata_id == MetadataORM.id, 
                            (MetadataORM.name == unicode(self.header[i])) & 
                            (MetadataValueORM.int_value == int(columns[i]))).one()
                    
                    elif meta.data_type == 3:
                        mv=self.store.find(MetadataValueORM, 
                            MetadataValueORM.metadata_id == MetadataORM.id, 
                            (MetadataORM.name == unicode(self.header[i])) & 
                            (MetadataValueORM.float_value == float(columns[i]))).one()

                    sample.metadata.add(mv)
                    
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

