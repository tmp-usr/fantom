
class HypothesisTester():
    
    def testGroups(self, method ,correction=""):
        self.method = method
        self.correction = correction



        if method == "Levene's Test":
            result= leveneTest(*groups)
        
        elif method == "Bartlet's Test":
            result= bartletTest(*groups)
        
        elif method == "Welch's t-test":
            result= tTest(*groups,var='unequal')
        
        elif method == "Student's t-test":
            result= tTest(*groups)
        
        elif method == "Mann-Whitney Test":
            result= mannWhitneyUTest(*groups)
        
        elif method == "Kruskal Wallis":
            result= kruskal(*groups)
        
        elif method == "Anova":
            result= anova(*groups)

        elif method == "Manova":
            #we might need rpy2 interaction here
            #result= manova(*groups)
            pass

        elif method == "Permanova":
            # same as above
            pass

        if result is not None:
            testStat= result[0]
            pValue= result[1]
            #self.testStatistics.append(result[0])
            #self.pValues.append(result[1])
        else:
            pass

        
        #if correction == "":
        #    self.correctedPValues = self.pValues
            
        #elif correction == "Bonferroni correction":
        #    self.correctedPValues = correctBonferroni(self.pValues)
        
        #elif correction == "False Discovery Rate":
        #    self.correctedPValues = correctBHFDR(self.pValues)
            
            
    #def filterComparison(self, pValue=1.0, mean = 0.0, foldChange= 0.0 ):
