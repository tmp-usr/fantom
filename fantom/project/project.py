from collections import namedtuple

from pandas import DataFrame
from storm.locals import Unicode, Int, Float, Reference

from fantom.src.launching.hierarchy_provider import HierarchyProvider
from fantom.src.sqling.project_selector import ProjectSelector
from fantom.src.sqling.project_updater import ProjectUpdater

class Project(object):
    
    def __init__(self, project_name, store, balter, file_provider, db_name= "", biodb_selector= None,  input_file_path="", transformation=None, metadata_file_path= None):
        """
            cancelled: a work-around method to initiate storm objects without arguments.
        """
        self.hierarchy_provider= HierarchyProvider(balter= balter, db_name= db_name, file_provider= file_provider, raw_file_path= input_file_path, biodb_selector= biodb_selector )
            
        self.data= self.hierarchy_provider.get_abundance_by_level(biodb_selector.getLevelCount())
        
        if metadata_file_path is not None:
            ProjectUpdater(project_name, store, metadata_file_path)

        self.project_selector= ProjectSelector(project_name, store)
        self.name= project_name
        self.samples= [Sample(sample.name, \
                Metadata(metadata)) for  \
                (sample.name, metadata) in \
                [(sample.name, self.project_selector.get_sample_metadata(sample.name)) for \
                sample in self.project_selector.get_all_samples()]]  
    
    #def set_db_hierarchy_level(self, level):
    #    self.data.set_level(level)        

    def get_samples(self):return self.samples
    
    @property
    def sample_names(self): return [s.name for s in self.samples]
    
    def get_samples_by_prop(self, prop, value, operator):
        samples= self.project_selector.get_samples_by_prop(prop, value, operator)
        return [sample for sample in self.samples if sample.name in [s.name for s in samples]]

    def get_categorical_samples(self):
        category_values= self.project_selector.get_categorical_samples()
        for category, value_samples in category_values.iteritems():
            for value, samples in value_samples.iteritems():
                category_values[category][value]= [sample for sample in self.samples if sample.name in [s for s in samples]] 
        
        return category_values    
    
    def __getitem__(self, sample_name):return [s for s in self.samples if s.name == sample_name][0]
    def __iter__(self):return iter(self.samples.iteritems())
    def __len__(self): return len(self.samples)
    
    def to_tsv(self):
        pass

    def update(self, *args, **kwargs):
        self.samples.update(*args,**kwargs)
   
    def get_metadata_categories(self):
        return self.samples[0].metadata.__dict__.keys()

    def metadata_to_data_frame(self):
        fields= self.get_metadata_categories()

        metadata_=[]
        frame= []
        index= self.sample_names
        for sample in self.samples:
            line= []
            for f in fields:
                line.append(sample.metadata[f])
            frame.append(line)
        return DataFrame(data= frame, columns=fields, index= index)
            

    def metadata_to_tsv(self, filepath):
        self.metadata_to_data_frame().to_csv(filepath, sep= "\t", index_label="Name")

    def metadata_to_biom(self):
        pass



class Sample(object):
        
    def __init__(self, name, metadata):
        self.name= name
        self.metadata= metadata

    def __getitem__(self, metadata_type):return self.metadata.__dict__[metadata_type]
    def __repr__(self): return self.name



class Metadata(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        
    
    def __getitem__(self, item): return self.__dict__[item]
    

