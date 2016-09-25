import os
import shutil

from pandas import DataFrame


class Report(object):
    
    def __init__(self, ssu_type, analysis_type, level):
        self.low_dir= ""
        self.high_dir=""
        self.gradient_dir=""
        
        self.level= level
        ### init outputs
        self.init_output_dirs(ssu_type, analysis_type, level,  root=".")
    
    


    def write_table(self, results, result_type, index_label, more=True, treatment=None):
        
        result_type= "padj_"+result_type
        if treatment is not None:
            direction = "more" if more else "less"
            output_file_base= "%s_%s_%.2f.xlsx" % (result_type, direction, treatment)   
            if treatment <= 10.0:
                output_file= os.path.join(self.low_dir, output_file_base)
            elif treatment > 10.0:
                output_file= os.path.join(self.high_dir, output_file_base)
            
        else:
            direction = "increasing" if more else "decreasing"
            output_file= os.path.join(self.gradient_dir, "%s_%s.xlsx" % (result_type, direction))  
        
        DataFrame(results).to_excel(output_file, index_label= index_label, header=True, float_format= "%.5g")        
        
    def write_abundance(self, taxon_ranks):
        output_file= os.path.join(self.analysis_dir, "abundance.xlsx")
        DataFrame(taxon_ranks).to_excel(output_file, index_label= self.level, header=True, float_format="%.5g")




trash="""

    def init_output_dirs(self, ssu_type, analysis_type, level, root="."):
        '''
            !!! handling of the previous result directories will be handled here
        '''
        
        self.output_dir_root= os.path.join(root, 'results_%s' % ssu_type) 
        self.analysis_dir = os.path.join(self.output_dir_root, "%s_%s" %(analysis_type, level))

        if os.path.exists(self.analysis_dir):
            shutil.rmtree(self.analysis_dir)
        
        self.low_dir= os.path.join(self.analysis_dir, 'low')
        self.high_dir= os.path.join(self.analysis_dir, 'high')
        self.gradient_dir= os.path.join(self.analysis_dir, 'gradient')

        os.makedirs(os.path.join(self.low_dir))
        os.makedirs(os.path.join(self.high_dir))
        os.makedirs(os.path.join(self.gradient_dir))






"""
