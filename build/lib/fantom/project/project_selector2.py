from collections import OrderedDict

from cached_property import cached_property

from project_base import ProjectBase, SampleORM, MetadataORM, SampleMetadataORM, MetadataValueORM


class Sample(object):
        
    def __init__(self,  name, metadata):
        self.name= name
        self.metadata= metadata

    def __getitem__(self, metadata_type):return self.metadata.__dict__[metadata_type]
    def __repr__(self): return self.name



class Metadata(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        
    def __getitem__(self, item): return self.__dict__[item]



class ProjectSelector(ProjectBase):
    def __init__(self, project_name, store):
        ProjectBase.__init__(self, project_name, store)
        
    
    def get_metadata_by_sample_name(self, sample_name):
        return self.samples[sample_name].metadata
    
    @cached_property
    def samples(self):
        """
            returns a dictionary with teh samples as the keys and metadata
        """
        
        self.sample_orms= self.store.find(SampleORM, SampleORM.project_id == self.project_orm.id )
        samples= OrderedDict()
        for sample_orm in self.sample_orms:
            
            
            sm= self.store.find(SampleMetadataORM, SampleMetadataORM.sample_id == sample_orm.id)
            
            metadata= dict()
            for sample_metadata in sm:
                mv= self.store.find(MetadataValueORM, MetadataValueORM.id == sample_metadata.metadata_value_id)
                for metadata_value in mv:
                    metadata_orm= self.store.find(MetadataORM, MetadataORM.id == metadata_value.metadata_id).one()
                    if metadata_orm.data_type == 1:
                        value= metadata_value.string_value
                
                    elif metadata_orm.data_type == 2:
                        value= metadata_value.int_value
            
                    elif metadata_orm.data_type == 3:
                        value= metadata_value.float_value

                    metadata[metadata_orm.name] = value
            sample= Sample(sample_orm.name, Metadata(**metadata))
            samples[sample.name]= sample
        return samples

    
    def get_sample_metadata_value(self, sample_name, metadata_name):
        return self.samples[sample_name][metadata_name]


    def get_metadata_names(self):
        return self.samples.items()[0][1].metadata.__dict__.keys()  


    def query_samples_by_metadata(self, metadata_name, metadata_value, operator):
        if operator == 'contains':
            return [sample for sample in self.samples.values() if metadata_value in sample.metadata[metadata_name]]
        elif operator == '=':

            return [sample for sample in self.samples.values() if sample.metadata[metadata_name] == metadata_value]
        
        elif operator == '<':
            return [sample for sample in self.samples.values() if sample.metadata[metadata_name] <  metadata_value]
        

        elif operator == '>':
            return [sample for sample in self.samples.values() if sample.metadata[metadata_name] >  metadata_value]
        

        elif operator == '<=':
            return [sample for sample in self.samples.values() if sample.metadata[metadata_name] <=  metadata_value]

        elif operator == '>=':
            return [sample for sample in self.samples.values() if sample.metadata[metadata_name] >=  metadata_value]
        
    def get_categorical_samples(self, metadata_name):
        categories = self.get_categorical_metadata()[metadata_name]
        categorical_samples= {}
        for category in categories:
            categorical_samples[category]= self.query_samples_by_metadata(metadata_name, category, "=")
        
        return categorical_samples
   
    

    def get_project_metadata(self):
        return [(metadata_orm, metadata_value_orm) for (metadata_orm,metadata_value_orm) in 
                self.store.find((MetadataORM, MetadataValueORM), 
             MetadataORM.id == MetadataValueORM.metadata_id,
             MetadataValueORM.id == SampleMetadataORM.metadata_value_id,
             SampleMetadataORM.sample_id == SampleORM.id,
             SampleORM.project_id == self.project_orm.id)]
    
    def get_metadata_values(self, metadata_name):
        values= {}
        for (md, mdv) in self.get_project_metadata():
            if md.name == metadata_name:
                if md.data_type == 1:
                    values[mdv.string_value] = 1
                elif md.data_type == 2:
                    values[mdv.int_value] = 1
                elif md.data_type == 3:
                    values[mdv.float_value] = 1
        return values.keys()
        

    def get_categorical_metadata(self):
        categorical_metadata= {}
        for md, mdv in self.get_project_metadata():
            if md.data_type == 1:
                if md.name not in categorical_metadata:
                    categorical_metadata[md.name] = []
                if mdv.string_value not in categorical_metadata[md.name]:
                    categorical_metadata[md.name].append(mdv.string_value)
        return categorical_metadata




trash= """

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




    #def convert_type(self, metadata):
    #    if self.get_metadata()[metadata.metadata.name] == 1:
    #        return metadata

    #    elif self.get_metadata()[metadata.metadata.name] == 2:
    #        setattr(metadata,value,Int())
    #        return metadata
    #    else:
    #        setattr(metadata,value,Float())
    #        return metadata

    
def get_categorical_samples():
        '''
            returns a dict with the keys as categories and values as samples.
        '''
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
        

ReferenceSet(Metadata.id, SampleMetadata.metadata_id, )


self.store.find(MetadataORM, 
             MetadataORM.id == SampleMetadataORM.metadata_id,
             SampleMetadataORM.sample_id == Sample.id,
             Sample.project_id == project_id)
    
    
    #_id==MetadataORM.id, 
    #        (SampleORM.name == unicode(sample_name)) & 
    #        (MetadataORM.name == unicode(metadata_name))).one()

"""
