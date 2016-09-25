from pandas import concat

class DataSummary(object):
    def __init__(self, data_frame):
        self.data_frame= data_frame.T

    @property
    def mean(self):
        mean=self.data_frame.mean()
        mean.name= "mean"
        return mean
        
    @property
    def std(self):
        std= self.data_frame.std()
        std.name= "std"
        return std

    #@property
    #def count(self):
    #    count= self.data_frame.sum()
    #    count.name= "count"
    #    return count

    @property
    def summary(self):
        return concat([self.mean, self.std], axis= 1)

# to be continued    
