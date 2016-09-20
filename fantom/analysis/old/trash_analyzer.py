
#def ApplyCorrelation(dataSet, metadata, corrType, pCutOff = 0.05, rCutOff = 0.00):
#    corrDataContent={}
#    i=0
#    for feature,v in dataSet.iteritems():
#        if corrType == 0:
#            result= pearsonCorr(metadata, v)
#        else:
#            result= spearmanCorr(metadata, v) 
#        
#        
#        if result[1] <= pCutOff and abs(result[0]) >= rCutOff: 
#            row=(feature, result[0],result[1])
#            corrDataContent[i] = row
#            i+=1 
#    return corrDataContent
