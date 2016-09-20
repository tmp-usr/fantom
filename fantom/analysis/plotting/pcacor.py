from matplotlib.mlab import PCA
from pandas import concat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from basicplot import BasicPlot
import matplotlib as mpl

### following classes incorporate metadata in the plots.


## issues to be analyzed
#1 input should be group container instead of data since we can access the individual group nnames and colors easier that way.

#2 3d and 2d options should be presented for the pca

#3 metadata based plotting should be included. when the main input source are the group containers, metadata can be accessed easier. 

import pdb

class PCAPlot(BasicPlot):
    def __init__(self, group_container, ascending_data = False, color_scheme= "YlGn", axes3d= False, fig_axes= (None, None), *args, **kwargs):
        self.color_scheme= color_scheme
        self.axes3d= axes3d
        
        BasicPlot.__init__(self, group_container, ascending_data, fig_axes= fig_axes, *args, **kwargs)    
   
        self.plot()
        self.polish(*args, **kwargs)
        self.legend()
        self.fig.savefig("a.png")
    
    def init_axes(self, fig=None, axes=None):
        if fig:
            self.fig, self.axes= fig, axes
        elif self.axes3d == False:
            self.fig, self.axes= plt.subplots(1, 1)
        else:
            self.fig= plt.figure()
            self.axes= Axes3D(self.fig)

    def plot(self):
        # data generation
        ### check if we need to merge according to the index of the biggest dataframe
        
        data= concat(self.data, axis= 1, join_axes= [self.data[0].index])
        
        sample_names= [d.columns for d in self.data]
      
        self.results= PCA(data, standardize=True)


        results= self.results.Y.T[:3]    

        len_samples= self.n_data

        n_colors= len(sample_names) 

        self.lines=[]
        for i in range(self.n_data):

            srange_left= sum([len(sample_names[s]) for s in range(i)]) 
            srange_right= sum([len(sample_names[s]) for s in range(i+1)])
            
            dim1= results[0][srange_left:srange_right]
            dim2= results[1][srange_left:srange_right]
            dims= [dim1, dim2]
            if self.axes3d:
                dim3= results[2][srange_left:srange_right]
                dims.append(dim3)

            
            line, = self.axes.plot(*dims, marker= "o", linestyle="None", \
                    alpha=self.alpha, color= self.group_container.groups[i].color)
            
            self.lines.append(line)
            self.axes.grid(True)
                



    def polish(self, *args, **kwargs):
        # title and label setting
        self.axes.set_xlabel('PC1 (%.2f%%)' % (self.results.fracs[0]*100))
        self.axes.set_ylabel('PC2 (%.2f%%)' % (self.results.fracs[1]*100))
        if self.axes3d:
            self.axes.set_zlabel('PC3 (%.2f%%)' % (self.results.fracs[2]*100))


    def legend(self):
        mpl.rcParams['legend.fontsize'] = 10
        leg= self.axes.legend( self.lines, [self.group_container[i].name for i in range(self.n_data)], ncol= self.n_data, loc=(0,1.02), fancybox=True )

