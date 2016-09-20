#import wx
import matplotlib
#from matplotlib.backends.backend_wxagg import \
#    FigureCanvasWxAgg as FigCanvas, \
#    NavigationToolbar2WxAgg as NavigationToolbar

import matplotlib.pyplot as plt   
#from matplotlib.mlab import prepca,center_matrix


import numpy as np
import scipy
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
import scipy.stats as st 

from matplotlib.patches import Rectangle,Polygon

import os

from basicplot import BasicPlot


class PieCircos(BasicPlot):
    def __init__(self, group_container, ascending_data, *args, **kwargs):
        BasicPlot.__init__(self, group_container, ascending_data, *args, **kwargs)

        ###
        self.plotall()
        self.polish(*args, **kwargs)
        self.legend()

    def init_axes(self):
        
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

    
    def polish(self, title ):
        """
            plots should be more square sized
        """

        #self.fig.suptitle(title, fontsize= self.title_font_size)
        #"""" Instead of writing a title just write the group names
        #     as the x axis label. 
        #     move the legend to top covering the top part of the 
        #     figure
        
        for i in range(len(self.axes)):
            ax= self.axes[i]
            
            ax.set_xlabel("Group %s" %i, size=10)





    def plotall(self):
        for i in range(self.n_data):
            self.plot(i)

    
    def legend(self):
        handles, labels = self.axes[0].get_legend_handles_labels()
        self.axes[0].legend(handles, labels= self.feature_names, ncol= self.n_data, loc= (0.0, 1.0), fontsize= "small")
        #self.fig.legend( self.legend_handles,  "upper right")
            
    
class Pie(PieCircos):
    def __init__(self, group_container, ascending_data= True, color_scheme= "Pastel1", *args, **kwargs): 
        self.color_scheme= color_scheme    
        
        PieCircos.__init__(self, group_container, ascending_data, *args, **kwargs)
    
    def plot(self, index):          
        
        data= self.data[index]
        ax= self.axes[index]

        means= data.T.mean()
        # color generation
        
        
        n_colors= len(means)
        
        cm = plt.get_cmap(self.color_scheme)
        colors = [cm(1.*i/n_colors, alpha= self.alpha) for i in range(n_colors)]
        

        # plotting
        patches, texts, auto_texts= ax.pie(means, autopct='%.1f%%', shadow=True, colors= colors)
        
        #self.legend_handles= patches 


class Circos(PieCircos):
    def __init__(self, group_container, ascending_data=True, *args, **kwargs):
        PieCircos.__init__(self, group_container, ascending_data, *args, **kwargs)
    
    def plot(self):
        pass
   


legend_lines= """       


    def set_size(self, w, h, forward=True):
        self.fig.set_size_inches(w, h, forward=forward)
        ## remember to set dpi while saving





# manual legend plotting and fontsize setting
        P=[]
        i=0
        for item in colors:
            p = Rectangle((0, 0), 5, 5, fc=item,alpha=0.5)
            P.append(p)
            i+=1
        nCol=0
        
        if NUM_COLORS < 10:
            nCol=NUM_COLORS/2
            loc=(0,-0.30)
        
        elif NUM_COLORS >= 10 and NUM_COLORS < 20:
            nCol=NUM_COLORS/3
            loc=(0,-0.40)
            
        elif NUM_COLORS >= 20 and NUM_COLORS < 30:
            nCol=NUM_COLORS/4
            loc=(0,-0.45)
        
        else:
            nCol=NUM_COLORS/6
            loc=(-0.15,-0.50)
        
        leg=ax1.legend(P, labels,ncol=nCol,fancybox=True,loc=loc)
        for t in leg.get_texts():
            t.set_fontsize('x-small')
"""
all_trash="""

        #

       
        # manual legend plotting 
        #P=[] 
        #for item in colors:
        #    p = Rectangle((0, 0), 5, 5, fc=item,alpha=0.5)
        #    P.append(p)
        
        #leg=ax1.legend(P, (group1, group2),ncol=2,fancybox=True,loc=(0,1.02))
        #for t in leg.get_texts():
        #    t.set_fontsize('small')  
        
        # drawing
        #self.canvas.draw()



        # new axes for the dendograms and the heatmap
        ## dendograms
        #ax1 = self.fig.add_axes([0.05,0.14,0.2,0.6])
        #ax2 = self.fig.add_axes([0.26,0.75,0.6,0.2]) 
        ## heatmap
        #axmatrix = self.fig.add_axes([0.26,0.14,0.6,0.6])
        ## colorbar
        #axcolor = self.fig.add_axes([0.06,0.83,0.18,0.04])
        
        # data generation/assignment 1
        #X=X.transpose()



#def qq(self, values):
#'''
#TODO: check if values can be a dataframe object 
#'''
# new axis 
#    ax1= self.single_axis()
# data generation/assignment
#    (osm, osr), (m, b, r) = st.probplot(values, dist='norm')  
#    osmf = osm.take([0, -1])     
#    osrf = m * osmf + b       
        
# plotting
#    ax1.plot(osm, osr, '.', osmf, osrf, '-')
# drawing
#    self.canvas.draw()

        #ax.set_xticks(range(len(tickColumns)))
        #ax.set_xticklabels(tickColumns,weight='ultralight',ha='right',rotation_mode='anchor', alpha=0.7 , rotation=25)
        #ax.set_yticks(range(len(tickRows)))
        #ax.set_yticklabels(tickRows,weight='ultralight',ha='left', alpha=0.7, style='italic')


        #ax.grid(True)
        # manual legend drawing
        #plt.figtext(0.70, 0.80, '* : '+group1 ,  color='red', weight='roman', size='small')
        #plt.figtext(0.70, 0.75, 'o : '+group2,  color='blue', weight='roman', size='small')
        
        # grids ???
        #l = ax.axhline( color='black', y=0, linestyle=':')
        #l = ax.axvline( color='black', x=0, linestyle=':')


        #if noLabel == True:
        #    sampleNames1=''
        #    sampleNames2=''
        #    group1=''
        #    group2=''


        # legend 
        #leg= ax.legend( (bars1[0], bars2[0]), (group1, group2),ncol=2,loc=(0,1.02),fancybox=True )
        #for t in leg.get_texts():
        #    t.set_fontsize('small') 
       

       
        # new axis
        #ax1, ax2= self.double_axes()



            #for t in leg1.get_texts():
            #    t.set_fontsize('x-small')  
        #

        # new axis
        #ax1,ax2= self.double_axes()

        # data generation
        #data = np.array(data)
        #data2=np.array(data2)       



        #

        # drawing
        #self.canvas.draw()


        # new axis
        #ax= self.single_axis()
        


        if legend:

            P1=[item for item in p]
            
            n_cols=0
            
            if n_colors < 10:
                n_cols= n_colors/2
                loc=(.2,-.3)
            
            elif n_colors >= 10 and n_colors < 20:
                n_cols= n_colors/4
                loc=(.1,-.4)
                
            elif n_colors >= 20 and n_colors < 30:
                
                n_cols= n_colors/5
                loc=(.1,-.45)
            
            else:
                
                n_cols= n_colors/6
                loc=(0,-.50)
         
        
            leg= ax.legend(P1, labels, loc=loc, ncol=n_cols, fancybox=True, fontsize= "x-small")
        


"""
