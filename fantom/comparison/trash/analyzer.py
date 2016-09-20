import math
import scipy.stats as st
import numpy as np
from pandas import DataFrame, Series 
from collections import namedtuple

msg1= '%s is a single group comparison test. Check the number of groups in the parameter and re-run.'
msg2= '%s is a two group comparison test. Check the number of groups in the parameter and re-run.'
msg3= '%s is a multiple group comparison test. Check the number of groups in the parameter and re-run.'

#### Correction

def correctBonferroni(pValues):
    ''' Bonferroni correction implementation '''    
    corrected = []
    for pValue in pValues:
      correctedValue = pValue * len(pValues)
      corrected.append(correctedValue)
    return corrected

def correctBHFDR(pValues):
    ''' Benjanimi-Hochberg FDR implementation '''
    indexedList = []
    index = 0
    for value in pValues:
      indexedList.append([value, index])
      index += 1
      
    indexedList.sort(reverse = True)

    nComparison = len(pValues)
    modifier = nComparison
    for i in range(len(indexedList)):
      index = indexedList[i][1]     
      pValues[index] = pValues[index] * nComparison / float(modifier)
      modifier -= 1
    return pValues


def compareIndexes(function, *groups):
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

def filterResults(Results, pvalue=0.05, mean= 0.0, foldchange=1):
    return Results[(Results['fdr'] <= pvalue) & 
                     (Results['mean1'] >= mean) &
                     (Results['mean2'] >= mean) &
                     (Results['foldchange'] >= foldchange )
                     ]


def tTest(*args ):
    
    if len(args) != 2:
        raise Exception(msg2 % 't-test')
   
    var= "equal"

    if var=='equal':
        return compareIndexes(st.ttest_ind, *args)
    else: # alternative would be var='unequal'
        return compareIndexes(welchTest, *args)

def welchTest(*args):
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
    df /= ((v1/n1)**2/(n1-1.) +(v2/n2)**2/(n2-1.))
    prob = st.t.sf(np.abs(t), df)*2
    return t, prob

def mannWhitneyUTest(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Mann Whitney U')
    return compareIndexes(st.mannwhitneyu, *args)

##  Tests for equal variances
def bartletTest(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Bartlet')
   
    return  compareIndexes(st.bartlett, *args)

def leveneTest(*args):
    if len(args) != 2:
        raise Exception(msg2 % 'Levene')
    return compareIndexes(st.levene, *args)

##  Tests for Normality

def shapiroTest(*args):
    if len(args) != 1:
        raise Exception(msg1 % 'Shapiro')

    return  st.shapiro(args)


#### Correlation
def pearsonCorr(x,y):
    return st.pearsonr(x,y)

def spearmanCorr(x,y):
    return st.spearmanr(x,y)


      

def ApplyCorrelation(dataSet, metadata, corrType, pCutOff = 0.05, rCutOff = 0.00):
    corrDataContent={}
    i=0
    for feature,v in dataSet.iteritems():
        if corrType == 0:
            result= pearsonCorr(metadata, v)
        else:
            result= spearmanCorr(metadata, v) 
        
        
        if result[1] <= pCutOff and abs(result[0]) >= rCutOff: 
            row=(feature, result[0],result[1])
            corrDataContent[i] = row
            i+=1 
    return corrDataContent
