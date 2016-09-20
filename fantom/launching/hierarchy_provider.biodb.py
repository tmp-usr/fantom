
from collections import OrderedDict


from pandas import read_csv, DataFrame, Series


from fantom.src.helper.pandas_data_types import panelToBasic, basicToPanel
from abundance_data import AbundanceData


import pdb


class HierarchicalAbundanceData(AbundanceData):
    def __init__(self, db_name, level, file_path, file_provider, selected_columns=[]):
        AbundanceData.__init__(self, db_name, file_path = file_path, selected_columns= selected_columns)
        
        self.db_name= db_name
        self.level= level
        self.file_provider= file_provider

    def set_level(self, level):
        level_file_path= self.file_provider.get_abundance_file_by_level(level)
        self.__init__(level=level, file_path = level_file_path, db_name= self.db_name, \
                file_provider= self.file_provider, selected_columns= self.selected_columns)
        #self.set_state()
 
    def __repr__(self):
        return self.data_frame.to_string()


class HierarchyProvider(object):
    """
        balter is a alternative for the biodb project.Check it out!
    """
    def __init__(self, file_provider, db_name, balter= None, biodb_selector= None, 
            raw_file_path="", sep= "\t", index_col="Name"):
        self.file_provider = file_provider
        main_file_path= self.file_provider.get_abundance_file_by_level("main")
        self.db_name= db_name

        if self.file_provider.exists(main_file_path):
            print """
            You have already built the hierarchy files.\ 
            Try accessing to individual hierarchy level abundances (self.get_by_level(level))!
            """
            pass

        else:
            self.balter= balter
            self.biodb_selector = biodb_selector
            
            self.db_hierarchy= None
            self.db_hierarchy_abundance= None

            df= read_csv(raw_file_path, sep=sep, dtype= {index_col: str})
            df= df.set_index(index_col)
        
            self.data_frame= self.raw_data_frame= df 
            self.build_hierarchy_levels()

    
    def build_hierarchy_levels(self):
        
        hierarchy_series= []
        uKOs= []
        nLevels= None
        
        
        for accession in self.data_frame.index:
            #feature=self.biodb_selector.get_feature_by_accession(unicode(accession))
            
            #import pdb
            
            ### TODO!!! This function will be replaced by a new one, surpassing the 
            # the extra time spent on lineage formation. 
            
            #lins= self.biodb_selector.get_lineages(feature)
            #balters= self.balter.get_hierarchy_by_accession(unicode(accession)) 
            
            if self.db_name == "ncbi":
                #print accession
                
                try:
                    taxon= self.biodb_selector.getFeatureByID(int(accession))
                except:
                    uKOs.append(accession)
                    continue
                lineage = self.biodb_selector.getLineage(taxon)
                balters= [lineage]
          

            else:
                feature= self.biodb_selector.getFeatureByAccession(unicode(accession))
                if feature is None:
                    continue
                balters= self.biodb_selector.getLineages2(feature)
           


            for balter in balters[feature]: 
               
                balter= list(balter)
                balter.insert(0, feature)
                
                #levels=  list(reversed(balter.hierarchy.split('|| ')))
               
                nLevels= len(balter) 
                levels= [f.name for f in balter if f.level in range(1,nLevels+1)]
                
                cols= []
                columns= []
                data= []
                s= None

               
                if self.db_name == "ncbi":
                    nLevels= 6
                    if len(levels) < nLevels:
                        continue

                    elif len(levels) >  nLevels:
                        ### an extreme case where the no rank is set to 
                        ### another level and the other rank and the updated
                        ### no rank taxa happen to exist in the same lineage.
                        ### we need to pop the extra no_rank lineage!
                        upd_levels= OrderedDict()
                        for feature in balter:
                            if feature.level not in upd_levels and feature.level in range(1,nLevels +1):
                                upd_levels[feature.level] = feature.name 
                        
                        levels= upd_levels.values()

                        
                cols= ["Level %d" % (i+1) for i in reversed(range(nLevels))]
                columns= cols + ['Accession'] + list(self.raw_data_frame.columns)
                data= levels + [accession] + list(self.data_frame.ix[accession])
                
                s=Series(data, columns)
                hierarchy_series.append(s)
            
            if len(balters) == 0:          
                rows= self.data_frame.ix[accession]
                
                if len(rows) > 1:
                    rows= self.data_frame.ix[accession].sum()
                
                mean= rows.mean()
                if mean > 100:
                    print accession, mean
                    uKOs.append(accession)
                        
        
        if len(uKOs) > 0:
            print "Identifiers listed below could not be found in the databse!"
            print "\",\"".join(map(str, uKOs))
            print "########"
       

        

        df= DataFrame(hierarchy_series)
        #try:
        panel= basicToPanel(df, nLevels)
        #except:
            
            #pdb.set_trace()
        
        self.set_db_hierarchy_abundance(panel)
        self.set_db_hierarchy(panel['db'])

        self.write_levels()

   
    def write_levels(self):
        """
            no need to write levels with enzymes. it will be the same size as the main dataframe
        """      
        
        df= panelToBasic(self.db_hierarchy_abundance)
       

        main_file_path= self.file_provider.get_abundance_file_by_level("main")
        
        df.to_csv(main_file_path, sep= "\t", index_label="Name")
        
        levels= [col for col in df.columns if col.startswith('Level')]
      

        for level in levels:
            
            n_level= int(level.lstrip("Level "))
        
            #selected_level= df.groupby([level]).sum()
            ### group by occasionally fails due to database entries.
            

            cols=[level] + [col for col in df.columns.tolist() if col not in levels]
            cols.remove("Accession")
            ##### groupby sum method adds also the strings together, so we
            ##### need to get rid of those columns which are the string
            ##### concatenation of the other columns.
            #df_grouped = df[cols].fillna(0).groupby(level).sum()
            df_grouped = df[cols].groupby(level).sum().fillna(0)
            #df_grouped = selected_level.aggregate(np.sum)[df.columns]
            level_file_path = self.file_provider.get_abundance_file_by_level(n_level)
            #print level_file_path
           
            #pdb.set_trace()
            df_grouped.to_csv(level_file_path, sep= "\t", index_label= "Name")

        self.db_hierarchy= None
        self.db_hierarchy_abundance= None
        self.data_frame= None
        
 
    def get_abundance_by_level(self, level):
        level_file_path= self.file_provider.get_abundance_file_by_level(level)
        return HierarchicalAbundanceData(db_name= self.db_name, level= level, file_path= level_file_path, file_provider= self.file_provider )
    
    def get_abundance_by_level_category(self, level, category):
        """
            DOES NOT WORK!!!
        """
        main_hier= self.get_abundance_by_level("main")
        return main_hier.data_frame.groupby('Level %i' %level).groups


    def get_db_hierarchy(self):return self.db_hierarchy
    def set_db_hierarchy(self, db_hierarchy):self.db_hierarchy = db_hierarchy
    
    def get_db_hierarchy_abundance(self): return self.db_hierarchy_abundance
    def set_db_hierarchy_abundance(self, db_hierarchy_abundance):
        self.db_hierarchy_abundance= db_hierarchy_abundance
