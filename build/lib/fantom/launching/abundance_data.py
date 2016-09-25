from pandas import read_csv

from data_transformer import DataTransformer
from fantom.src.analysis.summary import DataSummary


import pdb

class InputBase(object):
    
    def __init__(self, db_name="", file_path="", index_col= "Name", local= True):
        self.file_path = file_path
        self.local= local
        self.index_col= index_col
        self.db_name= db_name
        
        if file_path != "":
            #try:
            self.count_data_frame= read_csv(file_path, sep="\t", dtype= {"Name":str})
            self.count_data_frame= self.count_data_frame.set_index("Name")
            #except:
            print "There's a problem with the input file. Please check!"
                
        



class AbundanceData(InputBase):
    def __init__(self, db_name="", file_path="", transformation= "absolute", db_hierarchy=None, selected_columns= [], *args, **kwargs):
        InputBase.__init__(self, db_name=db_name, file_path= file_path, **kwargs)
        ### check if metadata is provided for all samples in the count data input
        #count_data_frame= self.count_data_frame
                
        self.transformer= DataTransformer(self.count_data_frame, transformation)
        self.data_frame= self.raw_data_frame= self.transformer.get_current_data_frame()
        self.summary= DataSummary(self.data_frame).summary
        #self.level= level
        #self.test= None
        if selected_columns == []:
            self.selected_columns= self.data_frame.columns
        else:
            self.selected_columns= selected_columns
            self.select(self.selected_columns)

        self.transformation= transformation
        #@property_pickled
    #def db_hierarchy(self, filepath):
    #    return self.db_hierarchy
    
    def select(self, cols):
        """
            deprecated: len cannot be a proxy to select subsets
            instead, we have to check if cols is a subset of the
            data_frame columns.
        """
        try:
            if set(cols).issubset(set(self.data_frame.columns)):
                self.data_frame= self.data_frame[cols]
            else:
                self.data_frame= self.raw_data_frame[cols]
        except:

            pdb.set_trace() 

        self.selected_columns= cols

    def to_transformed(self):
        self.data_frame= self.transformer.transformed
        self.select(self.selected_columns)
        return self.data_frame


    def to_absolute(self):
        self.data_frame= self.transformer.absolute
        self.select(self.selected_columns)
        return self.data_frame


    #def set_state(self):
    #    #self.select(self.selected_columns)
    #    if self.transformation:
    #        self.to_relative()
    #   
    #    else:
    #        self.to_absolute()


    def plot(self, plot_type="qq"):
        pass


    def describe(self):
        return self.data_frame.describe()






#!!!TODO: when taking the relative abundances: levels are divided by the normalized abundances according to the duplicated enzyme counts. consider calculating the relative abundances according to the total numbers in only the 4th level.


#from fantom.src.helper.file_provider import FileProvider
#from balter.balter import Balter


#db_name= "kegg_orthology"

#file_provider= FileProvider('periphyton',db_name)
#print file_provider['example']['abundance']

#balter= Balter(db_name, '/Users/kemal/repos/balter/data/balter.db')
#
#file_path= '/Users/kemal/repos/fantom/.files/example/abundance/' + file_provider['example']['abundance']
#had= HierarchicalAbundanceData( balter, file_provider, file_path)
#had.build_hierarchy_levels()
