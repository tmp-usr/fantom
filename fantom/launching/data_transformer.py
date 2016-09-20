import types
import pdb
import pandas 

absolute_function= lambda dataframe: dataframe.astype(float) # do nothing
relative_function=  lambda dataframe: dataframe.astype(float)/dataframe.astype(float).sum()

class DataTransformer(object):
    """
    count_data_frame: input for DataTransformer
    transformed_data_frame: transformed abundance data 
    """
    def __init__(self, count_data_frame, transformation= "absolute", transformation_function= None):
        
        self.absolute_data_frame= self.count_data_frame= count_data_frame
        self.transformed_data_frame= None
        self.current_data_frame= self.absolute_data_frame
        self.transformation= transformation
        self.transform(transformation, transformation_function)

    def transform(self, transformation, transformation_function = None):
        
        if transformation == "absolute":
            transformation_function = absolute_function
        elif transformation == "relative":
            transformation_function = relative_function
        else:
            if transformation_function is None:
               raise Exception("Transformation function must be of type 'function'!") 

        try:
            self.current_data_frame= self.count_data_frame.apply(transformation_function)
        
        except:
            pdb.set_trace()
        return self.current_data_frame
        
    def get_current_data_frame(self):
        return self.current_data_frame

    @property
    def transformed(self, transformation= "relative", transformation_function= None):
        self.transformation= transformation
        return self.transform(transformation, transformation_function)


    @property
    def absolute(self):
        self.transformation= "absolute"
        return self.transform(self.transformation)

    
