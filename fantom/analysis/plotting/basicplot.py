

class BasicPlot(object):
    """
        TODO: Organize the order of functions in plots. Stick to a clear ordering!!!!!
    
        core: comparative plots: bar, box, pie, area. start by bar and box
        plot type options are 
            box, bar, pie, area, dendogram, heatmap, pca    
            
    """
    def __init__(self, group_container, ascending_data, fig_axes= (None, None), *args, **kwargs): #canvas):
        

        #assert type(data) == list, "Please insert a list of data frames!"
        #self.fig = figure
        self.group_container= group_container
        self.data= group_container.get_data_frames()
        
        # sorting the data according to feature abundances
        
        df= self.data[0]
        new_df= df.T.mean().order(ascending= ascending_data)
        
        for i in range(len(self.data)):
            self.data[i]= self.data[i].ix[new_df.index]

        
        self.feature_names= self.data[0].index
        self.sample_names= self.data[0].columns

        ### general basic properties
        # sets the number of axes
        self.n_data= len(self.data) 
        # sets the y axes in most
        self.n_features= len(self.data[0].index)

        self.title_font_size= 15
        self.xlabel_font_size= 12
        self.ylabel_font_size= 12
        self.xtick_font_size= 10
        self.ytick_font_size= 10
        self.alpha= 0.6

        self.init_axes(*fig_axes)
        #self.init_properties()
        #self.plot_all()
        #self.polish(*args, **kwargs)


    def init_axes(self, fig=None, axes=None):
        pass
    
    def init_properties(self):
        pass

    def plot(self):
        pass

    def polish(self, *args, **kwargs):
        pass

    def legend(self):
        pass

    def plotall(self):
        pass







