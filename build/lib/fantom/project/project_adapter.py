import os

from models.objects.project import Metadata, MetadataValue, SampleMetadata, Sample


from storm.locals import *
from biom import load_table


def metadata_from_biom(biom_table_path, project_name, store):
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
        s= Sample(sample_id, Metadata)
        p.update({s.name: s})
    p.to_tsv()
    md= MetadataAdapter(p.name, store, p.tsv)


class ProjectAdapter(object):
    
    def __init__(self, project_name, store, metadata_file=None):
        
        self.store=store
        self.project_name=project_name

        self.header=[]
        self.Fields={}
        
        project=[p for p in self.store.find(Project, 
                 Project.name == unicode(self.project_name))]
       
        #new project
        if project == []:
            if metadata_file is not None:
                self.metadata_file=metadata_file
                self.project=self.create_new_project(self.project_name) 
                if self.project: 
                    self.load_metadata(self.metadata_file) 
                    self.insert_metadata_value()
                    self.insert_sample_metadata(self.metadata_file)
                    self.store.flush()
                else:
                    raise Exception
            
        #update project
        elif project != [] and metadata_file is not None:
            
            self.project=self.store.find(Project, 
                    Project.name == unicode(self.project_name)).one()
            
            self.metadata_file=metadata_file
            self.project.metadata_path = self.metadata_file
            
            self.load_metadata(self.metadata_file)
            self.update_metadata_value()
            self.insert_sample_metadata(self.metadata_file)
            self.store.flush()



    def create_project(self,project_name):       
        project=Project()
        project.name=project_name
        project.metadata_path=self.metadata_file
        if os.path.exists(str(project.metadata_path)):
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
            if k==0:
                samples= list(set([i for i in v]))
                for s in samples:
                    sample= self.store.find(Sample,Sample.name == unicode(s)).one()
                    if sample is None:
                        sample=Sample()
                        sample.name=unicode(s)
                        sample.project_id=self.project.id
                        self.store.add(sample)
            else:
                
                meta = self.store.find(Metadata, Metadata.name == unicode(self.header[k])).one()
                
                values= list(set([unicode(v) for v in v]))
                if meta is None:
                    meta=Metadata()
                    new_id=k
                    if lastInsert_id is not None:
                        new_id=lastInsert_id+k
                    
                    meta.id= new_id
                    meta.name= unicode(self.header[k])
                    meta.project_id= self.project.id 
                    types= list(set([type(i) for i in v]))
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
                    self.store.commit()
                
                for v in values:
                    if meta.data_type == 1:
                        mv=self.store.find(MetadataValue, 
                                (MetadataValue.metadata_id==meta.id) & 
                                (MetadataValue.string_value.like(unicode(v)))).one()
                        
                        if mv is None:
                            mv=MetadataValue()
                            mv.metadata_id=meta.id
                            mv.string_value=v
                            self.store.add(mv)
                        else:
                            self.store.find(SampleMetadata, 
                                    SampleMetadata.metadata_value_id== mv.id).remove()

                    elif meta.data_type == 2:
                        mv=self.store.find(MetadataValue, 
                                (MetadataValue.metadata_id==meta.id) & 
                                (MetadataValue.int_value == int(v))).one()
                        
                        if mv is None:
                            mv=MetadataValue()
                            mv.metadata_id=meta.id
                            mv.int_value=v
                            self.store.add(mv)
                        else:
                            self.store.find(SampleMetadata, 
                                    SampleMetadata.metadata_value_id==mv.id).remove()

                    elif meta.data_type == 3:
                        mv=self.store.find(MetadataValue, 
                                (MetadataValue.metadata_id==meta.id) & 
                                (MetadataValue.float_value == float(v))).one()
                        
                        if mv is None:
                            mv=MetadataValue()
                            mv.metadata_id=meta.id
                            mv.float_value=v
                            self.store.add(mv)
                        else:
                            self.store.find(SampleMetadata, 
                                    SampleMetadata.metadata_value_id==mv.id).remove()
            self.store.commit()

    def insert_metadata_value(self):
        #ids should be unique!!
        lastInsert_id=self.store.execute('SELECT MAX(id) FROM metadata').get_one()[0]
        for k,v in self.Fields.iteritems():
            if k==0:
                samples= list(set([i for i in v]))
                for s in samples:
                    sample=Sample()
                    sample.name=unicode(s)
                    sample.project=self.project
                    self.store.add(sample)
            else:
                meta=Metadata()
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
                    mv=MetadataValue()
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
            
            Sample.metadata = ReferenceSet(Sample.id,
                    SampleMetadata.sample_id,SampleMetadata.metadata_value_id,
                    MetadataValue.id)
            
            fMeta.readline()
            for line in fMeta:
                columns = line.rstrip().split('\t')
                sample=self.store.find(Sample,Sample.name == unicode(columns[0])).one()
                for i in range(1,len(columns)):
                    meta=self.store.find(Metadata, 
                            Metadata.name == unicode(self.header[i])).one()
                    if meta.data_type == 1:
                        mv=self.store.find(MetadataValue, 
                            MetadataValue.metadata_id == Metadata.id, 
                            (Metadata.name == unicode(self.header[i])) & 
                            (MetadataValue.string_value == unicode(columns[i]))).one()
                    
                    elif meta.data_type == 2:
                        mv=self.store.find(MetadataValue, 
                            MetadataValue.metadata_id == Metadata.id, 
                            (Metadata.name == unicode(self.header[i])) & 
                            (MetadataValue.int_value == int(columns[i]))).one()
                    
                    elif meta.data_type == 3:
                        mv=self.store.find(MetadataValue, 
                            MetadataValue.metadata_id == Metadata.id, 
                            (Metadata.name == unicode(self.header[i])) & 
                            (MetadataValue.float_value == float(columns[i]))).one()

                    sample.metadata.add(mv)
                    
            self.store.commit()
