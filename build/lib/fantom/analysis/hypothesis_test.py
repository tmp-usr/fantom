import numpy as np
from pandas import DataFrame,Series

from stats import correct_bonferroni, correct_fdr, correct_fdr_deprecated,\
            shapiro_test, corr_pearson, corr_spearman, bartlett_test, \
            levene_test, t_test, mann_whitney_test
from summary import DataSummary

import pdb


class HypothesisTest(object):
    
    def __init__(self, method, *data, **kwargs):
        self.data= data #[d for d in data]
        
        self.method= method
        self.n_groups = len(data)
        
        self.corrected=False
        self.p_values= dict()
        self.corrected_p_values= dict()
        self.test_stats= dict()
       
        if "group_indices" in kwargs:
            self.group_indices= kwargs["group_indices"]

    def test(self):
        """
            should be overridden
        """
        raise NotImplementedError

    def correct(self, method= "fdr"):
        #assert self.p_values != [], "First, run the test!"
        if method == "bonferroni":
            self.corrected_p_values= correct_bonferroni(self.p_values)
        elif method == "fdr":
            self.corrected_p_values= correct_fdr(self.p_values)
        self.correction_method= method
        self.corrected= True
        return self.corrected_p_values

    @property
    def results(self):
        #self.test()
        
        if not self.corrected:
            self.correct()

        test_stats= DataFrame(Series(self.test_stats), columns= ["test_stat"])
        p_values= DataFrame(Series(self.p_values), columns= ["p_value"])
        corrected_p_values= DataFrame(Series(self.corrected_p_values), columns= ["%s_corr_p_value" %self.correction_method])
        
        if self.n_groups > 1:
            summaries= [DataSummary(df).summary for df in self.data]
            df= summaries[0]
            for i in range(1, len(summaries)):
                df = df.join(summaries[i], rsuffix="_%s"% (i+1) )
            
        else:
            df= DataSummary(self.data[0]).summary() 
       

        df= df.join([test_stats, p_values, corrected_p_values])
        
        if self.n_groups >= 2:
            
            fold_change_ = np.log10(summaries[1]["mean"]) - np.log10(summaries[0]["mean"])
            df= df.assign(log_fold_change= fold_change_ )
        return df

    #@property
    def filter_results(self, p_value= 0.05, mean=2, abs_log_fold_change=0.1):
        
        ## property cachced can be useful for the result method above
        mean_columns=[col for col in self.results.columns if col.startswith("mean")]
        df=self.results

        exp= []
        for col in mean_columns:
            exp.append('%s >= %s' %(col, mean))
        mean_exp= ' & '.join(exp)
        
        df= df.query(mean_exp)  # &
                
        df= df[(abs(df['log_fold_change']) >= abs_log_fold_change) &
                (df['p_value'] <= p_value)
                
                ] 
        
        return df


class OneSampleTest(HypothesisTest):
    def __init__(self, method, *data):
        HypothesisTest.__init__(self, method, *data)
    
    def test(self):
        if self.method == "shapiro":
            self.test_stats, self.p_values, a= shapiro_test(self.data[0])


class Regression(HypothesisTest):
        
    def __init__(self):
        HypothesisTest.__init__(self, method, *data)

    def test(self):
        if self.method == "pearson":
            self.test_stats, self.p_values= corr_pearson(self.data[0], self.data[1])

        elif self.method == "spearman":
            self.test_stats, self.p_values= corr_spearman(self.data[0], self.data[1])



class TwoSampleTest(HypothesisTest):
    
    def __init__(self, method, *data, **kwargs):
        
        HypothesisTest.__init__(self, method, *data, **kwargs)
        self.test()
        self.filter_results()

    def test(self):
       
        indice_one= self.group_indices[0]
        indice_two= self.group_indices[1]


        if self.method == "levene":
            self.test_stats, self.p_values=  levene_test(self.data[indice_one], self.data[indice_two])

        elif self.method == "bartlett":

            self.test_stats, self.p_values=  bartlett_test(self.data[indice_one], self.data[indice_two])
        
        elif self.method == "t-test":
            self.test_stats, self.p_values= t_test(self.data[indice_one], self.data[indice_two])

        elif self.method == "mwu":
            self.test_stats, self.p_values= mann_whitney_test(self.data[indice_one], self.data[indice_two])
        

class MultiSampleTest(HypothesisTest):
    def __init__(self, method, *data):
        HypothesisTest.__init__(self, method, *data)
    
    def test(self):
        if self.method == "anova":
            pass

        elif self.method == "kruskal-wallis":
            pass


