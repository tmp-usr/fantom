from summary import DataSummary
from pandas import DataFrame
import numpy as np

class TestResult(object):
    def __init__(self, *data, **kwargs):
        self.data= data
        self.n_groups= len(self.data)

    def result(self):
        """
            mean, std, test_stats, p_values, corrected_p_values, fold_change
        """
        
        if self.n_groups > 1:
            summaries= [DataSummary(data_frame).summary() for data_frame in self.data]
            df= summaries[0]
            for i in range(1, len(summaries)):
                df = df.join(summaries[i], rsuffix="_%s"% (i+1) )
            if self.n_groups == 2:
                df.assign(fold_change= np.log2(summary1.mean) / np.log2(summary2.mean))

            return df

        else:
            return DataSummary(self.data[0]).summary() 

        
