import types

relative_function=  lambda dataframe: dataframe/dataframe.sum()

class DataTransformer(object):
    """
    count_data_frame: input for DataTransformer
    transformed_data_frame: transformed abundance data 
    """
    def __init__(self, count_data_frame, transformation= None):
        
        self.absolute_data_frame= self.count_data_frame= count_data_frame
        self.transformed_data_frame= None
        self.current_data_frame= self.absolute_data_frame

        if transformation == "absolute":
            pass
        
        elif transformation == "relative":
            self.current_data_frame= self.transformed_data_frame= self.transform(relative_function) 
            
        else:
            assert type(transformation) == types.FunctionType, "Transformations apart \
                    from relative and absolute have to be of type 'function'!"  
            self.transform(transformation)

    def transform(self, transformation_function):
        self.current_data_frame= self.transformed_data_frame= self.count_data_frame_frame.apply(transformation_function)
        return self.transformed_data_frame
   
    def get_current_data_frame(self):
        return self.current_data_frame

    
    def transformed(self):
        self.current_data_frame= self.transformed_data_frame
        return self.current_data_frame

    def absolute(self):
        self.current_data_frame= self.absolute_data_frame
        return self.current_data_frame
    
    #def get_data_frame(self):return self.data_frame
    #def set_data_frame(self, data_frame):self.data_frame=data_frame
    
