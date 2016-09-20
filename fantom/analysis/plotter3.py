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



class BasicPlot(object):
    """
        TODO: Organize the order of functions in plots. Stick to a clear ordering!!!!!
    
        core: comparative plots: bar, box, pie, area. start by bar and box
        plot type options are 
            box, bar, pie, area, dendogram, heatmap, pca    
            
    """
    def __init__(self, *data): #canvas):
        
        #self.fig = figure
        self.data= data
        
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


        self.init_axes()
        self.init_properties()
        self.plot_all()
        self.polish()


    def init_axes(self):
        pass
    
    def init_properties(self):
        pass

    def plot(self):
        pass

    def polish(self, *args, **kwargs):
        pass

    def legend(self):
        pass

    def plot_all(self):
        pass

class BarBox(BasicPlot):
    def __init__(self, *data):
        #same_axes = True
        BasicPlot.__init__(self, *data)

        self.box_width= 0.35
        self.y_positions= [np.arange(self.n_features)+ self.box_width * i for i in range(self.n_data)]
        


    def init_axes(self):

        """
            check if the same axes is gonna be used!
        
        """
        self.fig, self.axes= plt.subplots(1, 1)



    def polish(self, xlabel, ylabel, title):

        
        self.axes.tick_params(top=False,right=False,labelbottom=True,labeltop=False,labelleft=True,labelright=False,labelsize='small')
        self.axes.set_ylim(0, p.n_features )

        #magic equation
        self.axes.set_yticks((p.y_positions[0]-p.box_width) + (p.box_width * ( p.n_data + 1) /2 ))
        self.axes.set_yticklabels(p.feature_names, weight='normal',alpha=0.9, fontsize=9)


        self.axes.set_title(title, size= self.title_font_size)
        self.axes.set_xlabel(xlabel,size= self.xlabel_font_size)
        self.axes.set_ylabel(ylabel, size= self.ylabel_font_size)



class PieCircos(BasicPlot):
    def __init__(self, *data):
        BasicPlot.__init__(self, *data)
    
    def init_axes(self):
        
        if self.n_data < 4:
            n_rows= 1
            n_cols= n_plots

        elif self.n_data == 4:
            n_rows= 2
            n_cols= 2
        
        elif self.n_data > 4:
            n_rows= n_plots/3
            n_cols= 3

        self.fig, self.axes= plt.subplots(n_rows, n_cols, sharey= True)

    
    def polish(self, title ):
        self.fig.suptitle(title, fontsize= self.title_font_size)
         

        #ax.tick_params(top=False,right=False,labelbottom=True,labeltop=False,labelleft=True,labelright=False,labelsize='small')
        #ax.set_ylim(0, p.n_features )

        #magic equation
        #ax.set_yticks((p.y_positions[0]-p.box_width) + (p.box_width * ( p.n_data + 1) /2 ))
        #ax.set_yticklabels(p.feature_names, weight='normal',alpha=0.9, fontsize=9)


        #ax.set_title(title, size= 14)
        #ax.set_xlabel(xlabel,size=10)
        #ax.set_ylabel(ylabel, size=10)


class Area(PieCircos):
    def __init__(self, *data):
        PieCircos.__init__(self, *data)
    
    def polish(self):
        pass



class Box(BarBox):
    
    
    def __init__(self, *data):

        """
            check if the same axes is gonna be used!
        
        """
        BarBox.__init__(self, *data)


    def init_properties(self):
        ### this are only used in box and bars
        self.widths=[self.box_width] * self.n_features 
        

    def plot(self, index):

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
            
            box_polygon = Polygon(box_coords, facecolor= color, alpha=alpha)

            self.axes.add_patch(box_polygon)
    
class Bar(BarBox):
    
    
    def __init__(self, *data):
        BarBox.__init__(self, *data)

    def plot(self):

        data= data.T
        means= data.mean()
        std= data.std()

        #margin= index* self.box_width
        #tick_positions = np.arange(self.n_features)+ margin  # locations of the groups on the x axis

        # plotting
        bars = ax.barh(self.y_positions[index], means, self.box_width,   
                            xerr=std, 
                            color=color, 
                            alpha= alpha, 
                            error_kw=dict(ecolor='gray')
                            )
        
        # data ordering
        ax.invert_yaxis()





class BasicPlot(object):
    """
        TODO: Organize the order of functions in plots. Stick to a clear ordering!!!!!
    
        core: comparative plots: bar, box, pie, area. start by bar and box
        plot type options are 
            box, bar, pie, area, dendogram, heatmap, pca    
            
    """
    def __init__(self, *data): #canvas):
        
        #self.fig = figure
        self.data= data

        
        ### general basic properties
        # sets the number of axes
        self.n_data= len(self.data) 
        # sets the y axes in most
        self.n_features= len(self.data[0].index)

        ### axes initialization related properties
        #self.same_axes = same_axes
        #self.sharey= sharey

    
        #self.canvas = canvas 
        self.init_axes()
        

    def init_axes(self):

        """
            check if the same axes is gonna be used!
        
        """
        pass
        if self.same_axes:

            self.fig, self.axes= plt.subplots(1, 1)
        
        else:
            n_plots= len(self.data)
            
            if self.n_data < 4:
                n_rows= 1
                n_cols= n_plots

            elif self.n_data == 4:
                n_rows= 2
                n_cols= 2
            
            elif self.n_data > 4:
                n_rows= n_plots/3
                n_cols= 3

            self.fig, self.axes= plt.subplots(n_rows, n_cols, sharey= self.sharey)

   
    def init_variables(self):
        self.feature_names= self.data[0].index
        
    
    def init_properties(self):
        ### this are only used in box and bars
        self.box_width= 0.35
        

        self.widths= [self.box_width] * self.n_features 
        self.y_positions= [np.arange(self.n_features)+ self.box_width * i for i in range(self.n_data)]
        

    



    def bar(self, ax, data, color, index=0, alpha=0.5): 
        """
            todo: total redo!!!
        """
    def box(self, ax, data, color, index=0, alpha= 0.5): #group_names, log= False):
        """
            todo: 
                - data ordering and manual shape plotting is problematic. 
                - top 2 are colored differently. check carefully what N refers to below. 
        """



    def pie(self, ax, data, color_scheme= "Pastel1", alpha= 0.5):          
        
        means= data.T.mean()
        # color generation
        
        
        n_colors= len(means)
        
        cm = plt.get_cmap(color_scheme)
        colors = [cm(1.*i/n_colors, alpha= alpha) for i in range(n_colors)]
        

        # plotting
        p= ax.pie(means,  autopct='%.1f%%', shadow=True, colors= colors)






    def plot(self, p_type):
        for ax in self.axes:
            if p_type == "":
                pass

            elif p_type == "":
                pass

            elif p_type == "":
                pass

            elif p_type == "":
                pass

            elif p_type == "":
                pass


            elif p_type == "":
                pass

            elif p_type == "":
                pass
            
            elif p_type == "":
                pass



        #if log == True:
        #    data = np.log10(data)


        #ax.legend(handles= p)


#### TO BE REFACTORED


### TO BE REFACTORED


    def area(self, ax, labels, data, group, color_scheme= 'gist_rainbow', title= ""):
        """
            #works only for relative abundances
            sort accoring to means
            legend

        """
        #data= data.T

        for i in range(1,len(data)):
            data[i]=data[i]+data[i-1]
        
        data= np.insert(data, 0, 0, axis=0)

        max_value= np.max(data[-1])
        
        data=np.insert(data, len(data), max_value, axis=0)

        x=np.arange(len(data[1]))
        #

        n_colors = len(data)-1

        # color generator
        cm = plt.get_cmap(color_scheme)
        colors = [cm(1.*i/n_colors) for i in range(n_colors)]
        #

        ax.set_xlim(0,len(data[1])-1)
 
        ax.set_ylim(0,max_value)
        
        # plotting 
        for i in range(len(colors)):     
            ax.fill_between(x, data[i+1], data[i], color= colors[i], alpha=0.5)
        
        # tick parameters
        ax.tick_params(top=False,right=False,labeltop=False,labelright=False,labelsize='small')
        
        # label and title setting
        ax.set_xlabel("Samples",size=10)
        ax.set_ylabel("Relative Abundance",size=10)
        
        ax.set_title(title)



    


    def set_size(self, w, h, forward=True):
        self.fig.set_size_inches(w, h, forward=forward)
        ## remember to set dpi while saving



    def histogram(self, ax, x, bins):
        
        n, bins, patches = ax.hist(x,bins, facecolor='gray', alpha=0.75)
        
    
    def regression(self, ax, data, props, prop, feature):

        # data generation/assignment
        polycoeffs = scipy.polyfit(props, data, 1)
        yfit = scipy.polyval(polycoeffs, props)

        # plotting
        ax.plot(props, data, 'k.')
        ax.plot(props, yfit, 'r-')
        
        # axis labels
        ax.set_xlabel(prop, size="small")
        ax.set_ylabel(feature, size="small")
        
        # tick parameters
        ax.tick_params(top=False,right=False,labeltop=False,labelright=False,labelsize='x-small')
        # drawing
        #self.canvas.draw()


    def scatter(self, ax, x, y):
        ax.scatter(x, y)
        


   
    def set_labels(self, axes, xlabels, ylabels, title):
        pass



    def pca(self, data, group, noLabel=False,figPath=""):

        # data generation
        data_centered= center_matrix(data, dim = 0)
        
        a,b,c= prepca(data_centered)
        
        a1=a[0]
        a2=a[1]


             
        len_samples= len(samples)

        # plotting
        line, =ax.plot(a1[:len_samples], a2[:len_samples], "o", color= color,  picker=5)
        #

        # title and label setting
        ax.set_xlabel('PC1 (%.2f%%)' % (c[0]*100))
        ax.set_ylabel('PC2 (%.2f%%)' % (c[1]*100))
        
        # drawing
        #self.canvas.draw()
 

    def dendogram(self, ax, data, lblFeatures, lblSamples,figPath=""):    
        """
            todo: 
             arrange the tick params accoring to the orientation!!!
        """



        ## distance matrices for the dendograms
        D1=pdist(data, 'seuclidean')
        #D2=pdist(data.T, 'seuclidean')

        ## clustering and plotting the dendograms
        Y1 = sch.linkage(D1, method='average')
        Z1 = sch.dendrogram(Y1, orientation='right',labels=lblSamples)
       
        #plt.axis("off")
        #Y1 = sch.linkage(D1, method='complete')
        #Z1 = sch.dendrogram(Y1, labels=lblFeatures)
        
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')


        
        #ax.xaxis.set_major_locator(plt.NullLocator())
        
        
        # tick parameters 1
        #ax.set_xticks(None)
        #ax.set_yticks([])
        
        #ax.set_xticks([])
        #ax.set_yticks([])
        




    def heatmap(self, ax, data, sample_names, feature_names):
        
        ax_color= self.fig.add_axes([0.06,0.83,0.18,0.04])
       
        ## distance matrices for the dendograms
        D1=pdist(data, 'seuclidean')
        D2=pdist(data.T, 'seuclidean')

        ## clustering and plotting the dendograms
        Y1 = sch.linkage(D1, method='average')
        Z1 = sch.dendrogram(Y1, orientation='right',labels= sample_names)

        Y2 = sch.linkage(D2, method='complete')
        Z2 = sch.dendrogram(Y2, labels= sample_names)

        # data generation/assignment 2
        idx = Z1['leaves']
        tick_columns = Z1['ivl']

        idy = Z2['leaves']
        tick_rows = Z2['ivl']
        
        D = data[idx, :]
        D = D[:,idy]
        
        #D=np.log10(D)


        # plotting the heatmap
        im = ax.matshow(D, aspect='auto', cmap=plt.cm.YlOrRd)
        
        # tick parameters 2
        ax.tick_params(pad=2, labelbottom=True, labeltop=False, labelleft=False, labelright=True, labelsize='x-small'  )

    
        # plotting the colorbar
        cbar= plt.colorbar(im, cax= ax_color, orientation='horizontal')
        
        # tick parameters 3
        cbar.ax.tick_params(labelsize='x-small',top=False)
        cbar.ax.set_title('Color Key')
        ## Add the contour line levels to the colorbar
        ind = [-5,-3,-1]
        cbar.set_ticks(ind)
        
        # drawing 
        #self.canvas.draw()







legend_lines= """       # manual legend plotting and fontsize setting
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
