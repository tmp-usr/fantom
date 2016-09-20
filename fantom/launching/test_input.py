import pdb

from input_provider import AbundanceData


file_path= "/Users/kemal/tmp/pp_kegg_short.tsv"
db_name= "kegg_orthology"
index_col= "Name"

def test_input_reading():
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col)
    print a.count_data_frame
    
def test_absolute_transformation():
    ## absolute
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="absolute" )
    print ad.transformer.get_current_data_frame()

def test_relative_transformation():
    ## relative
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="relative" )
    print ad.transformer.get_current_data_frame()

def test_manual_transformation():
    ## manual transform
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="absolute" )
    print ad.transformer.transformed

def test_data_summary():
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="absolute" )
    print ad.summary

def test_abundance_data_transform():
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="absolute" )
    #pdb.set_trace()  
    print ad.to_transformed()

def test_abundance_data_absolute():
    ad= AbundanceData(file_path= file_path, db_name= db_name, index_col=index_col, transformation="absolute" )
    #pdb.set_trace()  
    ad.to_transformed()
    print ad.to_absolute()

def test_hierarchical_abundance():
    pass


#test_absolute_transformation()    
#test_relative_transformation()
#test_manual_transformation()
#test_data_summary()
#test_abundance_data_absolute()
