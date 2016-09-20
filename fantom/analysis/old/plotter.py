import wx
import matplotlib
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import matplotlib.pyplot as plt   
from matplotlib.mlab import prepca,center_matrix


import numpy as np
import scipy
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist
import scipy.stats as st 

from matplotlib.patches import Rectangle,Polygon

import os


ID=wx.ID_ANY


class Plotter(object):
    """
        TODO: Organize the order of functions in plots. Stick to a clear ordering!!!!!
    """
    def __init__(self, figure, canvas):
        
        self.fig = figure
        self.canvas = canvas 
        

    def qq(self, values):
        '''
            TODO: check if values can be a dataframe object 
        '''
        # new axis 
        ax1= self.single_axis()
        
        # data generation/assignment
        (osm, osr), (m, b, r) = st.probplot(values, dist='norm')  
        osmf = osm.take([0, -1])     
        osrf = m * osmf + b       
        
        # plotting
        ax1.plot(osm, osr, '.', osmf, osrf, '-')
        
        # drawing
        self.canvas.draw()
   

    def add_subplot(self, nrows, ncols, plot_number):
        self.fig.add_subplot(nrows, ncols, plot_number)

    def set_size(self, w, h, forward=True):
        self.fig.set_size_inches(w, h, forward=forward)
        ## remember to set dpi while saving

    def single_axes(self):
        #left, bottom, width, height
        self.fig.clear()
        return self.fig.add_subplot(111)

    def double_axes(self):
        #left, bottom, width, height
        self.fig.clear()
        return ax1, ax2
    
    def triple_axes(self):
        self.fig.clear()
        


    def histogram(self, x, bins):
        
        # new axis
        ax= self.single_axis()
        
        # plotting
        ax.hist(x,bins)
        
        # drawing
        self.canvas.draw()


    def regression(self, data, props, prop, feature):
        # new axis
        ax= self.single_axis()

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
        self.canvas.draw()


    def scatter(self, x, y):
        
        # new axis
        ax= self.single_axis()
        
        # plotting
        ax.scatter(x, y)
        
        # drawing
        self.canvas.draw()

        
    def pie(self, labels, fracs1,fracs2,group1,group2, title=''):
        
        # new axes
        ax1, ax2= self.double_axes()

        # color generation
        NUM_COLORS=len(fracs1)
        
        cm = plt.get_cmap('Pastel1')
        colors = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
        

        # plotting
        p1=ax1.pie(fracs1,  autopct='%.1f%%', shadow=True, colors=colors)
        p2=ax2.pie(fracs2,  autopct='%.1f%%', shadow=True,colors=colors)
         
        
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

        # title setting
        ax1.set_title(group1)
        ax2.set_title(group2)
        
        # drawing
        self.canvas.draw()

    
    def box(self, data1, data2, labels, group1, group2, color1, color2, log10=False):
       
        # new axis
        ax1, ax2= self.double_axes()

        # data generation assignment
        data1=np.array(data1).transpose()
        data2=np.array(data2).transpose()

    
        if log10==True:
            data1 = np.log10(data1)
            data2 = np.log10(data2)
            
        N=len(labels)
        width=0.35
        widths=[width] * N 
        ind=np.arange(N)+0.35
        
        # plotting
        bp1=ax1.boxplot(data1, vert=0, widths=widths,positions=ind+0.35)
        bp2=ax2.boxplot(data2, vert=0, widths=widths,positions=ind)
        
        medians = range(N)

        # manual shape plotting
        colors=[color1,color2]
        
        for i in range(N):
            box1 = bp1['boxes'][i]
            box1X = []
            box1Y = []
            box2 = bp2['boxes'][i]
            box2X = []
            box2Y = []
            for j in range(5):
                box1X.append(box1.get_xdata()[j])
                box1Y.append(box1.get_ydata()[j])
                box2X.append(box2.get_xdata()[j])
                box2Y.append(box2.get_ydata()[j])
            boxCoords1 = zip(box1X,box1Y)
            boxCoords2 = zip(box2X,box2Y)
            
            boxPolygon1 = Polygon(boxCoords1, facecolor=colors[0],alpha=0.5)
            boxPolygon2 = Polygon(boxCoords2, facecolor=colors[1],alpha=0.5)
            ax1.add_patch(boxPolygon1)
            ax2.add_patch(boxPolygon2)
        #

        # tick parameters
        ax1.tick_params(top=False,right=False,left=False,labeltop=False,labelright=False,labelsize='x-small')
        ax2.tick_params(top=False,right=False,left=False,labeltop=False,labelright=False,labelsize='x-small')
        
        ax1.set_yticks(ind+width/2)
        ax1.set_yticklabels(labels, weight='normal',alpha=0.9)
        ax1.set_ylim(0,N+0.1)
        
        ax1.set_xlabel("Relative Abundance",size=10)
        #

       
        # manual legend plotting 
        P=[] 
        for item in colors:
            p = Rectangle((0, 0), 5, 5, fc=item,alpha=0.5)
            P.append(p)
        
        leg=ax1.legend(P, (group1, group2),ncol=2,fancybox=True,loc=(0,1.02))
        for t in leg.get_texts():
            t.set_fontsize('small')  
        
        # drawing
        self.canvas.draw()



    def area(self,labels,data1,data2,group1,group2):
       
        # new axis
        ax1,ax2= self.double_axes()

        # data generation
        data1=np.array(data1)
        data2=np.array(data2)       
        
        for i in range(1,len(data1)):
            data1[i]=data1[i]+data1[i-1]
            data2[i]=data2[i]+data2[i-1]
        
        data1=np.insert(data1, 0, 0, axis=0)
        data2=np.insert(data2, 0, 0, axis=0)

        max1=np.max(data1[-1])
        max2=np.max(data2[-1])
        
        data1=np.insert(data1, len(data1), max1, axis=0)
        data2=np.insert(data2, len(data2), max2, axis=0)

        x1=np.arange(len(data1[1]))
        x2=np.arange(len(data2[1]))
        #

        NUM_COLORS = len(data1)-1

        # color generator
        cm = plt.get_cmap('gist_rainbow')
        colors = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
        #

        
        ax1.set_xlim(0,len(data1[1])-1)
        ax2.set_xlim(0,len(data2[1])-1)
        
        
        ax1.set_ylim(0,max1)
        ax2.set_ylim(0,max2)
        
        # plotting 
        for item in colors:     
            ax1.fill_between(x1,data1[i+1],data1[i],color=item,alpha=0.5)
            ax2.fill_between(x2,data2[i+1],data2[i],color=item,alpha=0.5)
        
        # tick parameters
        ax1.tick_params(top=False,right=False,labeltop=False,labelright=False,labelsize='small')
        ax2.tick_params(top=False,right=False,left=False,labeltop=False,labelright=False,labelsize='small')
        
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
        #

        # label and title setting
        ax1.set_xlabel("Samples",size=10)
        ax2.set_xlabel("Samples",size=10)
        ax1.set_ylabel("Relative Abundance",size=10)
        ax2.set_ylabel("Relative Abundance",size=10)
        
        ax1.set_title(group1)
        ax2.set_title(group2)
        #

        # drawing
        self.canvas.draw()
   
    def set_labels(self, axes, xlabels, ylabels, title):
        pass


    def bar(self,labels,group1, group2,means1,means2,std1,std2,color1,color2):
        
        # new axis
        ax= self.single_axis()
        

        N = len(means1)
        
        ind = np.arange(N)  # locations of the groups on the x axis
        width = 0.35      # widths of bars
        
        
        # label and title setting
        ax.set_xlabel("Relative Abundance",size=10)
        

        # tick parameters
        ax.tick_params(top=False,right=False,labelbottom=True,labeltop=False,labelleft=True,labelright=False,labelsize='x-small')
        ax.set_yticks(ind+width)
        ax.set_yticklabels(labels, weight='normal',alpha=0.9 )
        
        # plotting
        bars1 = ax.barh(ind, means1, width,
                            color=color1,alpha=0.5,
                            xerr=std1)
        

        bars2 = ax.barh(ind+width, means2, width,
                            color=color2,alpha=0.5,
                            xerr=std2)
        

        # legend 
        leg= ax.legend( (bars1[0], bars2[0]), (group1, group2),ncol=2,loc=(0,1.02),fancybox=True )
        for t in leg.get_texts():
            t.set_fontsize('small') 
       
        # data ordering
        ax.invert_yaxis()

        # drawing
        self.canvas.draw()
           


    def pca(self, data, group1, group2, featureNames=[], sampleNames1=[], sampleNames2=[], noLabel=False,figPath=""):
        # new axis
        ax= self.single_axis()
        
        # data generation
        data_centered= center_matrix(data, dim = 0)
        
        a,b,c=prepca(data_centered)
        
        a1=a[0]
        a2=a[1]

        if noLabel == True:
            sampleNames1=''
            sampleNames2=''
            group1=''
            group2=''
             
        len1=len(sampleNames1)
        
        # plotting
        line1,=ax.plot(a1[:len1], a2[:len1], "r*", picker=5)
        line2,=ax.plot(a1[len1:], a2[len1:], 'bo', picker=5)
        #

        # manual legend drawing
        plt.figtext(0.70, 0.80, '* : '+group1 ,  color='red', weight='roman', size='small')
        plt.figtext(0.70, 0.75, 'o : '+group2,  color='blue', weight='roman', size='small')
        
        # grids ???
        l = ax.axhline( color='black', y=0, linestyle=':')
        l = ax.axvline( color='black', x=0, linestyle=':')

        # title and label setting
        ax.set_xlabel('PC1 (%.1f%%)' % (c[0]*100))
        ax.set_ylabel('PC2 (%.1f%%)' % (c[1]*100))
        
        # drawing
        self.canvas.draw()
 

    def dendograms_heatmap(self, X,lblFeatures,lblSamples,figPath=""):    
        # new axes for the dendograms and the heatmap
        ## dendograms
        ax1 = self.fig.add_axes([0.05,0.14,0.2,0.6])
        ax2 = self.fig.add_axes([0.26,0.75,0.6,0.2]) 
        ## heatmap
        axmatrix = self.fig.add_axes([0.26,0.14,0.6,0.6])
        ## colorbar
        axcolor = self.fig.add_axes([0.06,0.83,0.18,0.04])
        
        # data generation/assignment 1
        X=X.transpose()
        
        ## distance matrices for the dendograms
        D1=pdist(X.transpose(), 'seuclidean')
        D2=pdist(X, 'seuclidean')

        ## clustering and plotting the dendograms
        Y2 = sch.linkage(D2, method='average')
        Z2 = sch.dendrogram(Y2, orientation='right',labels=lblSamples)
        
        Y1 = sch.linkage(D1, method='complete')
        Z1 = sch.dendrogram(Y1, labels=lblFeatures)
        
        
        # tick parameters 1
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        ax2.set_xticks([])
        ax2.set_yticks([])

        
        # data generation/assignment 2
        idy = Z1['leaves']
        tickColumns = Z1['ivl']

        idx = Z2['leaves']
        tickRows = Z2['ivl']
        
        D = X[idx,:]
        D = D[:,idy]
        
        D=np.log10(D)
        
        # plotting the heatmap
        im = axmatrix.matshow(D, aspect='auto', cmap=plt.cm.YlOrRd)
        
        # tick parameters 2
        axmatrix.tick_params(pad=2,labelbottom=True,labeltop=False,labelleft=False,labelright=True,labelsize='x-small'  )
        axmatrix.set_xticks(range(len(tickColumns)))
        axmatrix.set_xticklabels(tickColumns,weight='ultralight',ha='right',rotation_mode='anchor', alpha=0.7 , rotation=25)
        axmatrix.set_yticks(range(len(tickRows)))
        axmatrix.set_yticklabels(tickRows,weight='ultralight',ha='left', alpha=0.7, style='italic')
    
        # plotting the colorbar
        cbar= plt.colorbar(im, cax=axcolor,orientation='horizontal', extend='both')
        
        # tick parameters 3
        cbar.ax.tick_params(labelsize='x-small',top=False)
        cbar.ax.set_title('Color Key')
        ## Add the contour line levels to the colorbar
        ind = [-5,-3,-1]
        cbar.set_ticks(ind)
        
        # drawing 
        self.canvas.draw()
