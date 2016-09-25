from hypothesis_test import OneSampleTest, TwoSampleTest, MultiSampleTest


class Analysis(object):
    """
        analysis_type: one sample, two-samples, multiple-samples 
        method: analysis method including the comparative tests and explorartory methods
        groups: subjected groups
        table: result table
        plot: result plot

    """
    
    def __init__(self, group_container):
        self.group_container= group_container
        #self.project= project 
        #
        self.analysis_type= ""
        self.method = ""
        
        self.report= None
        
        #self.table= None
        #self.plot= None
        #
        #self.stats= None

    
    def test(self, analysis_type, analysis_method, group_indices=[0,1]):
        """
            assert that the data are at the same database 
            hierarchy level. throw an exception otherwise.
        """
        
        data_frames= self.group_container.get_data_frames()
        

        if analysis_type == "two-sample":
            self.test_runner= TwoSampleTest(analysis_method, group_indices= group_indices, *data_frames)
            

        elif analysis_type == "multi-sample":
            self.test_runner= MultiSampleTest(analysis_method, *data_frames)
        
        return self.test_runner.results
        
        

    def means(self):
        """
        returns the means and standard deviations of the group data
        """
        pass
    
    def plot(self, plot_type):
        pass
    

    #def to_relative(self):
    #    self.group_container.to_relative()

    #def to_absolute(self):
    #    self.group_container.to_absolute()

    #def set_db_hierarchy_level(self, level):
    #    self.group_container.set_db_hierarchy_level(level)
    
    def build_report(self):
        pass




