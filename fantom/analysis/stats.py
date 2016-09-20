import math
from collections import namedtuple, OrderedDict

import scipy.stats as st
import numpy as np
from pandas import DataFrame, Series 


msg1= '%s is a single group comparison test. Check the number of groups in the parameter and re-run.'
msg2= '%s is a two group comparison test. Check the number of groups in the parameter and re-run.'
msg3= '%s is a multiple group comparison test. Check the number of groups in the parameter and re-run.'

#### Correction

def correct_bonferroni(p_values):
    """ Bonferroni correction
        p_values: keys, index ; values, p_value 
    """
    corrected_p_values = dict()
    for index, pValue in p_values.iteritems():
      corrected_p_values[index] = pValue * len(p_values)
    return dict(corrected_p_values)


def correct_fdr_deprecated(p_values):
    ''' Benjanimi-Hochberg FDR '''
    indexedList = []
    index = 0
    for value in p_values:
      indexedList.append([value, index])
      index += 1
      
    indexedList.sort(reverse = True)

    nComparison = len(p_values)
    modifier = nComparison
    for i in range(len(indexedList)):
      index = indexedList[i][1]     
      p_values[index] = p_values[index] * nComparison / float(modifier)
      modifier -= 1
    return p_values


def correct_fdr(p_values):
    """ Benjamini-Hochberg FDR
        p_values: keys, index ; values, p_value 
    """
    p_values= OrderedDict(p_values)
    nComparison= len(p_values)
    modifier= nComparison
    
    indexed_p_values= OrderedDict({(j[1],i):j[0] for i, j in enumerate(p_values.items())})
    
    indexed_p_values= OrderedDict(sorted(indexed_p_values.items(), reverse=True))
    
    #print indexed_p_values
    for (value, i),ind in indexed_p_values.items():
        #print i,ind    
        p_values[ind]= p_values[ind] * nComparison / float(modifier)
        modifier -= 1
    
    #print p_values
    return dict(p_values)



def welch_test(*args):
    ''' calculates welch's t-test for unequal sample sizes and unequal variances'''
    
    if len(args) != 2:
        raise Exception(msg2 % 'Welch\'s')
    
    x1 = np.mean(a)
    x2 = np.mean(b)
    v1 = np.var(a)
    v2 = np.var(b)
    n1 = len(a)
    n2 = len(b)
    t = (x1-x2)/np.sqrt(v1/n1 + v2/n2)
    df  = (v1/n1 + v2/n2)**2
    df /=  ((v1/n1)**2/(n1-1.) +(v2/n2)**2/(n2-1.))
    prob = st.t.sf(np.abs(t), df)*2
    return t, prob


def t_test(*args ):
    
    if len(args) != 2:
        raise Exception(msg2 % 't-test')
   
    var= "equal"

    if var=='equal':
        return st.ttest_ind(*args)
    else: # alternative would be var='unequal'
        return welch_test(*args)

def test_individual(function, *args):
    test_stats={}
    p_values= {}
    for index in args[0].index:
        try:
            test_stat, p_value= function(args[0].ix[index], args[1].ix[index])
            test_stats[index]= test_stat
            p_values[index]= p_value
        except Exception, e:
            print e
    return test_stats, p_values

def mann_whitney_test(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Mann Whitney U')
    return test_individual(st.mannwhitneyu, *args)

##  Tests for equal variances
def bartlett_test(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Bartlet')
    return st.bartlett(*args)

def levene_test(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Levene')
    return st.levene(*args)

##  Tests for Normality

def shapiro_test(*args):
    if len(args) != 1:
        raise Exception(msg1 % 'Shapiro')

    return  st.shapiro(args)


#### Correlation
def corr_pearson(x,y):
    return st.pearsonr(x,y)

def corr_spearman(x,y):
    return st.spearmanr(x,y)







def compare_indexes_deprecated(function, *groups):
    g1= groups[0]
    g2= groups[1]
    Results=[]
    Result=namedtuple('Result','index pvalue teststat mean1 std1 mean2 std2 foldchange')
    
    for index, samples in g1.iterrows():
        sample1=samples
        sample2=g2.ix[index]
        mean1= sample1.mean()
        mean2= sample2.mean()
        std1= sample1.std()
        std2= sample2.std()
        foldchange= abs(mean1/mean2) if abs(mean1) > abs(mean2) else abs(mean2/mean1)
        try:
            tstat, pvalue= function(sample1, sample2)
        except:
            tstat, pvalue= 0, 0
        Results.append(Result(index, pvalue, tstat, mean1, std1, mean2, std2, foldchange))
    
    ResultDf= DataFrame(Results, columns= Result._fields).set_index('index')
    ResultDf['bonferroni']= Series(correctBonferroni(ResultDf['pvalue']), index=ResultDf.index)
    ResultDf['fdr']= Series(correctBHFDR(ResultDf['pvalue']), index=ResultDf.index)
    pdb.set_trace()
    return ResultDf

def filter_results_deprecated(Results, pvalue=0.05, mean= 0.0, foldchange=1):
    return Results[(Results['fdr'] <= pvalue) & 
                     (Results['mean1'] >= mean) &
                     (Results['mean2'] >= mean) &
                     (Results['foldchange'] >= foldchange )
                     ]



