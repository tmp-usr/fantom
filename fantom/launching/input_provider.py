from pandas import read_csv

from data_transformer import DataTransformer
from fantom.src.analysis.summary import DataSummary

class InputBase(object):
    
    def __init__(self, db_name="", file_path="", index_col= "Name"):
        self.db_name= db_name
        self.file_path = file_path
        self.index_col= index_col
        
        if file_path != "":
            try:
                self.count_data_frame= read_csv(file_path, sep="\t", index_col=index_col)
            except:
                print "There's a problem with the input file. Please check!"


        ### check if metadata is provided for all samples in the count data input
        ### if not remove those samples or give a warning!


class AbundanceData(InputBase):
    def __init__(self, transformation= None, db_hierarchy=None, selected_samples= [], level=None, *args, **kwargs):
        InputBase.__init__(self, **kwargs)
        self.transformer= DataTransformer(self.count_data_frame, transformation)
        self.data_frame= self.raw_data_frame= self.transformer.get_current_data_frame()
        self.summary= DataSummary(self.data_frame).summary
        self.level= level
        #self.test= None
        if selected_samples == []:
            self.selected_samples= self.data_frame.columns
        else:
            self.selected_samples= selected_samples
        
    def select_samples(self, sample_names): #select in the previous version!
        """
            deprecated: len cannot be a proxy to select subsets
            instead, we have to check if cols is a subset of the
            data_frame columns.
        """
        
        #if set(sample_names).issubset(set(self.data_frame.columns)):
        self.data_frame= self.data_frame[sample_names]
        #else:
        #    self.data_frame= self.raw_data_frame[sample_names]
        self.selected_samples= sample_names

    def to_transformed(self):
        self.data_frame= self.transformer.transformed
        self.select_samples(self.selected_samples)
        #self.transformation= "relative"
        return self.data_frame

    def to_absolute(self):
        self.data_frame= self.transformer.absolute
        self.select_samples(self.selected_samples)
        return self.data_frame

    def describe(self):
        return self.data_frame.describe()


class HierarchicalAbundanceData(AbundanceData):
    def __init__(self, level, file_path, file_provider, selected_samples=[]):
        AbundanceData.__init__(self, file_path = file_path, selected_columns= selected_columns)
        self.level= level
        self.file_provider= file_provider

    def set_level(self, level):
        level_file_path= self.file_provider.get_abundance_file_by_level(level)
        self.__init__(level=level, file_path = level_file_path, \
                file_provider= self.file_provider, selected_columns= self.selected_columns)
        #self.set_state()

