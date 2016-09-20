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

from matplotlib.patches import Rectangle, Polygon


import os

from basicplot import BasicPlot


class BarBox(BasicPlot):
    def __init__(self, group_container, ascending_data, *args, **kwargs):
        
        BasicPlot.__init__(self, group_container, ascending_data, *args, **kwargs)
        ####same_axes = True
        self.box_width= 0.35
        self.widths=[self.box_width] * self.n_features 
        self.y_positions= [np.arange(self.n_features)+ self.box_width * i for i in range(self.n_data)]
        
        self.legend_handles= []

        ###
        self.plotall()
        self.polish(*args, **kwargs)
        self.legend()
        

    def init_axes(self):

        """
            check if the same axes is gonna be used!
        
        """
        self.fig, self.axes= plt.subplots(1, 1)



    def polish(self, title):

       
        xlabel = "Relative abundance"
        ylabel= ""
        self.axes.tick_params(top=False,right=False,labelbottom=True,labeltop=False,labelleft=True,labelright=False,labelsize='small')
        self.axes.set_ylim(0, self.n_features )

        #magic equation
        self.axes.set_yticks((self.y_positions[0]-self.box_width) + (self.box_width * ( self.n_data + 1) /2 ))
        self.axes.set_yticklabels(self.feature_names, weight='normal',alpha=self.alpha, fontsize= self.ytick_font_size)


        self.axes.set_title(title, size= self.title_font_size)
        self.axes.set_xlabel(xlabel,size= self.xlabel_font_size)
        self.axes.set_ylabel(ylabel, size= self.ylabel_font_size)

    
    def plotall(self):
        for i in range(self.n_data):
            self.plot(i, "green")



    def legend(self):
        leg=self.axes.legend( handles= self.legend_handles, fontsize= "small", fancybox=True, loc=(1.02, 0.8))
        

    def legendBox(self):
        ### previously used for BOX
        # manual legend plotting 
        P=[] 
        for item in co:
            p = Rectangle((0, 0), 5, 5, fc=item, alpha=self.alpha)
            P.append(p)
        
        leg=ax1.legend(P, (group1, group2), ncol=2,fancybox=True,loc=(0,1.02))
        for t in leg.get_texts():
            t.set_fontsize('small') 
    
    def legendBar(self):
        ### previously used for BOX
        # legend 
        leg= ax.legend( (bars1[0], bars2[0]), (group1, group2),ncol=2,loc=(0,1.02),fancybox=True )
        for t in leg.get_texts():
            t.set_fontsize('small')

    def legendArea(self):
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


    def legendPie(self):
        # legend positioning and font size setting
        P1=[item for item in p1]
        
        nCol=0
        
        if NUM_COLORS < 10:
            nCol=NUM_COLORS/2
            loc=(.2,-.3)
        
        elif NUM_COLORS >= 10 and NUM_COLORS < 20:
            nCol=NUM_COLORS/4
            loc=(.1,-.4)
            
        elif NUM_COLORS >= 20 and NUM_COLORS < 30:
            
            nCol=NUM_COLORS/5
            loc=(.1,-.45)
        
        else:
            
            nCol=NUM_COLORS/6
            loc=(0,-.50)
        
        
        leg1=ax1.legend(P1, labels, loc=loc,ncol=nCol,fancybox=True)
        
        
        for t in leg1.get_texts():
            t.set_fontsize('x-small')  
        #




class Box(BarBox):
    
    
    def __init__(self, group_container, ascending_data=True, *args, **kwargs):

        """
            check if the same axes is gonna be used!
        
        """
        
        BarBox.__init__(self, group_container, ascending_data, *args, **kwargs)
        
    def init_properties(self):
        pass
        ### this are only used in box and bars
        

    def plot(self, index, color):

        data= self.data[index]
        ### transform data
        data= np.array(data.T)

        # plotting
        bp= self.axes.boxplot(data, vert=0, widths=self.widths, positions= self.y_positions[index])
            
        # manual shape plotting
                    
        for i in range(self.n_features):
            box = bp['boxes'][i]
            whisker= bp['whiskers'][i]
            
            box.set_color(color)
            whisker.set_color("gray")
        

            boxX = []
            boxY = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            box_coords = zip(boxX,boxY)
            
            box_polygon = Polygon(box_coords, facecolor= color, alpha=self.alpha)

            self.axes.add_patch(box_polygon)
        
        
        ### required for the legend

        p = Rectangle((0, 0), 5, 5, fc=color, alpha=self.alpha, label= "group %s" %index )
        self.legend_handles.append(p) 


class Bar(BarBox):
    
    
    def __init__(self, group_container, ascending_data= True, *args, **kwargs):
        BarBox.__init__(self, group_container, ascending_data, *args, **kwargs)

    
    def plot(self, index, color):
        
        data= self.data[index]
        data= data.T
        means= data.mean()
        std= data.std()

        #margin= index* self.box_width
        #tick_positions = np.arange(self.n_features)+ margin  # locations of the groups on the x axis

        # plotting
        bars = self.axes.barh(self.y_positions[index], means, self.box_width,   
                            xerr=std, 
                            color=color, 
                            alpha= self.alpha, 
                            error_kw=dict(ecolor='gray'),
                            label= "group %s" % index
                            )
        
        p = Rectangle((0, 0), 5, 5, fc=color, alpha=self.alpha, label= "group %s" %index )
        self.legend_handles.append(p) 
        
        # data ordering
        #self.axes.invert_yaxis()



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
