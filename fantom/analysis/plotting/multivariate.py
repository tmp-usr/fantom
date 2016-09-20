import matplotlib.pyplot as plt
from matplotlib import ticker
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist

from basicplot import BasicPlot 

class Dendogram(BasicPlot):
    def __init__(self, group_container, ascending_data = False, samples= True, ticks= True, fig_axes= (None, None), *args, **kwargs):
        BasicPlot.__init__(self, group_container, ascending_data, fig_axes= fig_axes, *args, **kwargs)    
        
        self.samples= samples
        self.ticks= ticks
        self.dendogram= {}
    
        self.plotall()
        self.polish(*args, **kwargs)
        self.legend()

    
    def init_axes(self, fig= None, axes= None):

        if fig:
            self.fig, self.axes= fig, [axes]
    
        else:
            
            if self.n_data < 4:
                n_rows= 1
                n_cols= self.n_data

            elif self.n_data == 4:
                n_rows= 2
                n_cols= 2
            
            elif self.n_data > 4:
                n_rows= n_plots/3
                n_cols= 3

            self.fig, self.axes= plt.subplots(n_rows, n_cols, sharey= True)
            if n_rows == 1 and n_cols == 1:
                self.axes = [self.axes]
    
    def plot(self, index):
        ## distance matrices for the dendograms
        ax= self.axes[index]
        data= self.data[index]
     
        if self.samples:
            data=data.T
            names= data.columns
            orientation = "right"
        
        else:
            orientation= "top"
            names= data.T.columns
        
        distance_matrix=pdist(data, 'seuclidean')
        #D2=pdist(data.T, 'seuclidean')

        ## clustering and plotting the dendograms
        linkages = sch.linkage(distance_matrix, method='average')
        self.dendogram = sch.dendrogram(linkages, orientation= orientation, labels= names, ax= ax )
        

    def plotall(self):
        for i in range(self.n_data):
            self.plot(i)
    
    def polish(self, title):
        
        self.fig.suptitle(title, fontsize= self.title_font_size)
        
        for i in range(len(self.axes)):
            ax= self.axes[i]
            if self.samples and self.ticks:
                ax.set_xticks([])
                if i < len(self.axes):
                    ax.set_yticks([])

            elif not self.samples and self.ticks:
                ax.set_yticks([])
                ax.set_xticklabels(ax.get_xticklabels(), rotation= 25, 
                       ha='right',  rotation_mode='anchor',
                       fontsize= "small")

            elif not self.ticks:
                ax.set_yticks([])
                ax.set_xticks([])



class Heatmap(BasicPlot):
    def __init__(self, group_container, ascending_data = False, color_scheme= "YlOrRd", fig_axes= (None, None), ax_colorbar= None, *args, **kwargs):
        
        if len(data) > 1:
            raise Exception, "Heatmap is an exploratory plot for one sample/group!"
        
        self.color_scheme= color_scheme 
        BasicPlot.__init__(self, group_container, ascending_data, fig_axes= fig_axes, *args, **kwargs)    
        

        self.plot(ax_colorbar)
        self.polish(*args, **kwargs)
        self.legend()

    
    def init_axes(self, fig=None, axes=None):
        if fig:
            self.fig, self.axes= fig, axes
        else:
            self.fig, self.axes= plt.subplots(1, 1)

    
    def plot(self, ax_colorbar= None):
        data= self.data[0]
        cm = plt.get_cmap(self.color_scheme)
        im= self.axes.matshow(data, aspect='auto', cmap= cm )
        self.axes.grid(False)
        if ax_colorbar:
            self.cbar= plt.colorbar(im, cax=ax_colorbar, orientation='horizontal') 
                                    #aspect=10)#, pad= -1.1)
        else:
            self.cbar= plt.colorbar(im, orientation='horizontal', shrink=0.3, 
                                    aspect=10)#, pad= -1.1)


    def polish(self):
        ### polish the heatmap
        self.axes.tick_params(pad=2,labelbottom=True,labeltop=False,
                                    labelleft=False,labelright=True,
                                    labelsize='x-small',
                                    left= False, top=False)
        
        data= self.data[0]
        self.axes.set_xticks(range(len(data.columns)))
        self.axes.set_xticklabels(data.columns, weight='ultralight',ha='right',
                                rotation_mode='anchor', rotation=25)
        
        self.axes.set_yticks(range(len(data.index)))
        self.axes.set_yticklabels(data.index,weight='ultralight',ha='left', 
                                 alpha=0.7, style='italic')

        ### polish the colorbar
        self.cbar.ax.tick_params(labelsize='x-small',top=False)
        self.cbar.ax.set_title('Abundance', fontsize="small")
        
        ### restrict the number of ticks to 3
        tick_locator = ticker.MaxNLocator(nbins=4)
        self.cbar.locator= tick_locator
        self.cbar.update_ticks()
 
        # Add the contour line levels to the colorbar
        #ind = [-5,-3,-1]
        
        #self.cbar.set_ticks(ind)
    


class HeatmapDendogram(object):
    def __init__(self, group_container, ascending_data=False, *args, **kwargs ):
        #BasicPlot.__init__(self, data, ascending_data, *args, **kwargs)    
        self.init_axes()
        dend1= Dendogram(data, ascending_data = False, samples= True, ticks= False, title= "", fig_axes= (self.fig, self.ax_samples), *args, **kwargs)    
        dend2= Dendogram(data, ascending_data = False, samples= False, ticks= False, title= "", fig_axes= (self.fig, self.ax_features), *args, **kwargs)    
         
        sample_names=dend1.dendogram['leaves'] 
        feature_names= dend2.dendogram['leaves']

        data= data[0].T.ix[sample_names, feature_names]

        heatmap = Heatmap([data], ascending_data = False, color_scheme= "YlOrRd", fig_axes= (self.fig, self.ax_heatmap), ax_colorbar= self.ax_colorbar,*args, **kwargs)
        

    def init_axes(self):
        self.fig= plt.figure()
        self.ax_samples = self.fig.add_axes([0.05,0.14,0.2,0.6])
        self.ax_features = self.fig.add_axes([0.26,0.75,0.6,0.2])
        
        self.ax_colorbar= self.fig.add_axes([0.06,0.83,0.18,0.04])
        self.ax_heatmap = self.fig.add_axes([0.26,0.14,0.6,0.6])



