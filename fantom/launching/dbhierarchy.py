import os

import numpy as np
from pandas import DataFrame, Series, read_csv

from biodb.sqling.selector import Selector

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper


class DBHierarchyWriter(object):
    def __init__(self):
        pass




class DBHierarchy(object):
    
    def __init__(self, db_name, abundance_data_file_path, project_name= "unnamed", index_col= "Name"):
        
        self.abundance_data= AbundanceData(db_name, abundance_data_file_path, index_col="Name" )
        
        self.project_name= project_name
        self.db_name= db_name
        
        self.biodb_selector= Selector(db_name)

        self._build_hier_levels()


    def select_by_level(self, level, transformation):
        
        csvFile= file_provider.get_abundance_file_by_level(level, transformation)

        df= read_csv(csvFile, sep="\t").set_index('Level %s' %level)
    
        return HierarchicalAbundanceData(count_data_frame= df, transformation= None )

    def _build_hier_levels(self):
        """
            placing the abundance data into database hierarchy levels
            TODO!!!: compare the performance of this function with 
                     pacfm.building.assembler.assemble_ideograms!!!
        """

        main_count_file_path= file_provider.get_abundance_file_by_level("main")
        
        enz_types= ["with_enzymes","without_enzymes"]
        norms= ["relative","absolute"]
        
        uKOs=[]
        nLevels=0
            
        hier_series= []
        if not file_provide.exists(main_count_file_path):    
            for accession in self.abundance_frame.index:
                try:
                    feature=self.biodb_selector.get_feature_by_accession(unicode(accession))
                    lins= self.biodb_selector.get_lineages(feature)
                    for k,values in lins.iteritems():
                        for v in values:
                            levels=  v.split('; ')
                            levels.insert(0, k)
                            nLevels= len(levels)
                            cols= ["Level %d" % (i+1) for i in range(len(levels))]
                            columns= cols + ['Accession']+ list(self.abundance_data.data_frame.columns)
                            data= list(reversed(levels))+[accession]+list(self.abundance_frame.ix[accession])
                            s=Series(data,columns)
                            hier_series.append(s)

                
                except AttributeError:
                    uKOs.append(accession)
                
                
                df=DataFrame(hier_series)

                df.to_csv(main_count_file_path, sep='\t')

        else:
            df= read_csv(fam_file,sep='\t')
            #nLevels= len([c for c in df.columns if c.startswith('Level')])

        levels= [col for col in df.columns if col.starts_with('Level')]

        for level in leveles:
            
            n_level= int(level.lstrip("Level "))
            
            selected_level= df.groupby([level])
            df_grouped = selected_level.aggregate(np.sum)[df.columns]
            
            level_file_path= file_provider.get_abundance_file_by_level(n_level)


        
        #for enz_type in enz_types:
        #    for relative in norms:
        #        for level in range(nLevels):
        #            level+=1
        #            self._select_by_level(df, nLevels, level, enz_type, relative)


        if len(uKOs) > 0:
            print '%d features out of %d could not be found in the database!' %(len(uKOs), len(self.abundance_frame.index))
            print 'Please check your feature abundance input file for the lines starting with following feature accession codes: '+';'.join(uKOs)   
                

    #def _save_abundance_by_level(self, df, level):
        
        #dirPath="%s/tables/%s/%s/" %(self.project_name, self.db_name, show_enzymes)
        #n_levels= len(levels)
        
        #if show_enzymes == 'with_enzymes':
        #    selected_level= df.groupby(['Level %s' %level, "Level %d" %nLevels, "Accession"])
        #else:
    #   selected_level= df.groupby(['Level %s' %level])
        
        
        #if relative == 'relative':
        #    normF= lambda x:x/x.sum()
        #    df_grouped=df_grouped.apply(normF)
        #    dirPath+= 'relative/'
        
        #ielse:
        #    dirPath+= 'absolute/'

        #df_grouped.to_csv('%slevel%s.tsv' % (dirPath,level),sep='\t', float_format= "%.2g")
    #    return df_grouped


    def get_children(self):
        if self.curLevel not in self.Children:
            self.Children[self.curLevel]=self.biodb.getChildrenByLevel(self.curLevel)

    def get_lineage_by_name(self,featureName):
        feature=self.current_features[str(featureName)]
        return self.biodb.getLineages(feature)


