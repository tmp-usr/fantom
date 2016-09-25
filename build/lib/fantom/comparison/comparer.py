from fantom import stats as st 

class Comparer(object):

    def __init__(self, gb):
        if len(gb) == 1:
            self.comparison_type= "one"

        if len(gb) == 2:
            self.comparison_type= "pair" 
        
        if len(gb) > 2:
            self.comparison_type= "multiple"
        
        self.groups= gb.groups
        
        self.method=None
        self.plot= None
        self.test_stats=None
        self.p_values=None

    def compare(self, method):
            
        self.method= method
        groups= [group.fam for group in self.groups]
        
        if method == "Student's t-test" or method == 'ttest':
            Result= st.tTest(*groups)
        
        elif method == "Mann-Whitney Test" or method == 'mwu':
            Result= st.mannWhitneyUTest(*groups)
             
        elif method == "Kruskal Wallis":
            Result= st.kruskal(*groups)
        
        elif method == "Anova":
            Result= st.anova(*groups)

        elif method == "Manova":
            #we might need rpy2 interaction here
            #result= manova(*groups)
            pass

        elif method == "Permanova":
            # same as above
            pass
        

        FilteredResult= st.filter_results(Result)
        return FilteredResult



