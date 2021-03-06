from storm.locals import Unicode, Int, Float, Reference, ReferenceSet

from fantom.sqling.project_orm import SampleORM, ProjectORM, MetadataORM, SampleMetadataORM, MetadataValueORM

class ProjectSelector(object):
    
    def __init__(self, project_name, store):
        self.store= store
        self.project= self.store.find(ProjectORM, ProjectORM.name == unicode(project_name)).one()


    def get_all_metadata(self, categorical=False):

        samples= self.store.find(SampleORM, SampleORM.project_id == self.project.id )
        
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
                self.project.id)]


    def convert_type(self, metadata):
        if self.get_metadata()[metadata.metadata.name] == 1:
            return metadata

        elif self.get_metadata()[metadata.metadata.name] == 2:
            setattr(metadata,value,Int())
            return metadata
        else:
            setattr(metadata,value,Float())
            return metadata



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
    


    def get_all_samples(self):
        
        SampleORM.metadata = ReferenceSet(SampleORM.id,
                SampleMetadataORM.sample_id, 
                SampleMetadataORM.metadata_value_id,
                MetadataValueORM.id)
        
        return [sample for sample in self.store.find(SampleORM, 
            SampleORM.project_id == self.project.id)]


    def get_categorical_samples(self):
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
        

    def get_prop_values(self, prop):
        return list(set([[[str(value) for value in (metadata.string_value,metadata.int_value,metadata.float_value) if value is not None ][0] for metadata in sample.metadata if metadata.metadata.name == unicode(prop)][0] for sample in self.get_all_samples()]))


    def get_sample_metadata(self, sample_name):
        
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
            

    def get_sample_metadata_by_name(self, sample_name, metadata_name):        
        return self.store.find(SampleMetadataORM, 
            SampleMetadataORM.sample_id == SampleORM.id,
            SampleMetadataORM.metadata_value_id == MetadataValueORM.id,
            MetadataValueORM.metadata_id==MetadataORM.id, 
            (SampleORM.name == unicode(sample_name)) & 
            (MetadataORM.name == unicode(metadata_name))).one()
        

    def get_categorical_metadata(self):
        return [ metadata for metadata,data_type in
                self.get_metadata().iteritems() if data_type == 1]


    def get_samples_by_prop(self, prop, value, operator):
        
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

    def to_tsv(self):
        pass


