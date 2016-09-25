from pandas import read_csv,DataFrame,Series
from plumbing.cache import property_cached

from data_transformer import DataTransformer
from summary import DataSummary
from fantom.src.helper.pandas_data_types import panelToBasic, basicToPanel
#from balter.balter import Balter 

class InputBase(object):
    
    def __init__(self, db_name="", file_path="", index_col= "Name", local= True):
        self.file_path = file_path
        self.local= local
        self.index_col= index_col
        self.db_name= db_name
        
        if file_path != "":
            try:
                self.count_data_frame= read_csv(file_path, sep="\t", index_col=index_col)
            except:
                print "There's a problem with the input file. Please check!"
                
        



class AbundanceData(InputBase):
    def __init__(self, count_data_frame, transformation= None, db_hierarchy=None, selected_columns= [], *args, **kwargs):
        InputBase.__init__(self, **kwargs)
        ### check if metadata is provided for all samples in the count data input
        count_data_frame= self.count_data_frame
                
        self.transformer= DataTransformer(count_data_frame, transformation)
        self.data_frame= self.raw_data_frame= self.transformer.data_frame
        self.summary= DataSummary(self.data_frame).summary
        #self.level= level
        #self.test= None
        if selected_columns == []:
            self.selected_columns= self.data_frame.columns
        else:
            self.selected_columns= selected_columns
        
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
        
        if set(cols).issubset(set(self.data_frame.columns)):
            self.data_frame= self.data_frame[cols]
        else:
            self.data_frame= self.raw_data_frame[cols]
        
        self.selected_columns= cols

    #@property_cached
    def to_relative(self):
        self.data_frame= self.transformer.relative
        self.select(self.selected_columns)
        self.transformation = 1
        return self.data_frame


    #@property_cached
    def to_absolute(self):
        self.data_frame= self.transformer.absolute
        self.select(self.selected_columns)
        self.transformation= 0
        return self.data_frame


    def set_state(self):
        #self.select(self.selected_columns)
        if self.transformation:
            self.to_relative()
       
        else:
            self.to_absolute()

    def plot(self, plot_type="qq"):
        pass


    def describe(self):
        return self.data_frame.describe()


class HierarchicalAbundanceData(AbundanceData):
    def __init__(self, level, file_path, file_provider, selected_columns=[]):
        AbundanceData.__init__(self, file_path = file_path)
        self.level= level
        self.file_provider= file_provider

    def set_level(self, level):
        level_file_path= self.file_provider.get_abundance_file_by_level(level)
        self.__init__(level=level, file_path = level_file_path, \
                file_provider= self.file_provider, selected_columns= self.selected_columns)
        self.set_state()



class HierarchyProvider(object):
    """
        db_hierarchy: a dataframe involving the hierarchies of the db identifiers
        db_hierarchu: a datapanel involving the database hierarchy and the abundance information 
    """
    
    def __init__(self, file_provider, balter=None, raw_file_path="", sep= "\t", index_col="Name"):
       
        self.file_provider= file_provider
    
        main_file_path= self.file_provider.get_abundance_file_by_level('main')
        #print main_file_path 

        if self.file_provider.exists(main_file_path):    
            print "You have already built the hierarchy files. Try accessing to individual \
hierarchy level abundances (self.get_by_level(level))!"
            print "Check file path: %s " %main_file_path
            pass

        else:
            self.balter = balter
            self.db_hierarchy= None
            self.db_hierarchy_abundance= None

            self.data_frame= self.raw_data_frame= read_csv(raw_file_path, sep=sep, index_col= index_col)
            self.build_hierarchy_levels()

        #self.data= self.get_abundance_by_level()

    def get_db_hierarchy(self):return self.db_hierarchy
    def set_db_hierarchy(self, db_hierarchy):self.db_hierarchy = db_hierarchy
    
    def get_db_hierarchy_abundance(self): return self.db_hierarchy_abundance
    def set_db_hierarchy_abundance(self, db_hierarchy_abundance):
        self.db_hierarchy_abundance= db_hierarchy_abundance


    #@property
    #def db_hierarchy_abundance(self):
        

    def build_hierarchy_levels(self):
        
        hierarchy_series= []
        uKOs= []
        nLevels= None
        for accession in self.data_frame.index:
            try:
                #feature=self.biodb_selector.get_feature_by_accession(unicode(accession))
                
                
                ### TODO!!! This function will be replaced by a new one, surpassing the 
                # the extra time spent on lineage formation. 
                
                #lins= self.biodb_selector.get_lineages(feature)
                balters= self.balter.get_hierarchy_by_accession(unicode(accession)) 
                for balter in balters: 
                    levels=  list(reversed(balter.hierarchy.split('|| ')))
                    
                    if nLevels == None:
                        nLevels= len(levels)
                    
                    cols= ["Level %d" % (i+1) for i in range(len(levels))]
                    columns= cols + ['Accession'] + list(self.raw_data_frame.columns)
                    data= levels + [balter.accession] + list(self.data_frame.ix[accession])
                    s=Series(data, columns)
                    hierarchy_series.append(s)

            except Exception,e:
                print e
                uKOs.append(accession)
                        
        
        df= DataFrame(hierarchy_series)
        panel= basicToPanel(df, nLevels)
        self.set_db_hierarchy_abundance(panel)
        self.set_db_hierarchy(panel['db'].dropna(axis=1))
        
        self.write_levels()

        #panel= basicToPanel(df, nLevels )
        #self.set_db_hierarchy(panelToBasic(panel)['db'].dropna(axis=1))
       

    def write_levels(self):
        """
            no need to write levels with enzymes. it will be the same size as the main dataframe
        """      
        df= panelToBasic(self.db_hierarchy_abundance)
        main_file_path= self.file_provider.get_abundance_file_by_level("main")
        
        df.to_csv(main_file_path, sep= "\t", index_label="Name")
        
        levels= [col for col in df.columns if col.startswith('Level')]
        
        for level in levels:
            
            n_level= int(level.lstrip("Level "))
        
            #selected_level= df.groupby([level]).sum()
            df_grouped = df.groupby([level]).sum()
            #df_grouped = selected_level.aggregate(np.sum)[df.columns]
            level_file_path = self.file_provider.get_abundance_file_by_level(n_level)
            #print level_file_path
            df_grouped.to_csv(level_file_path, sep= "\t", index_label= "Name")

        self.db_hierarchy= None
        self.db_hierarchy_abundance= None
        self.data_frame= None
        
 

    def get_abundance_by_level(self, level):
        level_file_path= self.file_provider.get_abundance_file_by_level(level)
        return HierarchicalAbundanceData(level= level, file_path= level_file_path, file_provider= self.file_provider )
    
    
    


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
