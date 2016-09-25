from collections import namedtuple

from pandas import DataFrame
from storm.locals import Unicode, Int, Float, Reference
from cached_property import cached_property

#from fantom.launching.hierarchy_provider import HierarchyProvider
from fantom.project.project_selector2 import ProjectSelector
#from fantom.sqling.project_updater import ProjectUpdater

class Project(object):
    
    def __init__(self, project_name, store, file_provider= None, db_name= "", biodb_selector= None,  input_file_path="", transformation=None, metadata_file_path= None):
        """
            cancelled: a work-around method to initiate storm objects without arguments.
        """
#       self.hierarchy_provider= HierarchyProvider(balter= balter, db_name= db_name, file_provider= file_provider, raw_file_path= input_file_path, biodb_selector= biodb_selector )
            
#        self.data= self.hierarchy_provider.get_abundance_by_level(biodb_selector.getLevelCount())
        
        #if metadata_file_path is not None:
        #    ProjectUpdater(project_name, store, metadata_file_path)

        self.project_selector= ProjectSelector(project_name, store)
        self.samples= self.project_selector.samples
        self.name= project_name
    
    #def set_db_hierarchy_level(self, level):
    #    self.data.set_level(level)        

    def get_samples(self):return self.samples
   
    @cached_property
    def sample_names(self): return self.project_selector.samples.keys()
    
    def query_samples_by_metadata(self, metadata_name, metadata_value, operator):
        return self.project_selector.query_samples_by_metadata(metadata_name, metadata_value, operator)

    def get_categorical_samples(self, category):
        return self.project_selector.get_categorical_samples(category)
    
    def __getitem__(self, sample_name):return self.samples[sample_name]
    def __iter__(self):return iter(self.samples.iteritems())
    def __len__(self): return len(self.samples)
    
    def to_tsv(self):
        pass

    def update(self, *args, **kwargs):
        self.samples.update(*args,**kwargs)
   
    def get_metadata_names(self):
        return self.project_selector.get_metadata_names()

    def metadata_to_data_frame(self):
        fields= self.get_metadata_names()
        metadata_=[]
        frame= []
        index= []
        for sample_name, sample in self.samples.iteritems():
            line= []
            for f in fields:
                line.append(sample.metadata[f])
            frame.append(line)
            index.append(sample_name)
        return DataFrame(data= frame, columns=fields, index= index)
            

    def metadata_to_tsv(self, filepath):
        self.metadata_to_data_frame().to_csv(filepath, sep= "\t", index_label="Name")

    def metadata_to_biom(self):
        pass



    

from storm.locals import *


fantomii_db= "../project/fantomii.db"

fantom_sqlite_db = create_database("sqlite:%s" % fantomii_db )
store= Store(fantom_sqlite_db)

ps = Project("a", store)


