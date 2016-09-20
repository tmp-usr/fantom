from biom import load_table
from pandas import DataFrame


class BiomParser(object):
    def __init__(self, biom_file_path):
        self.biom_file_path= biom_file_path
        self.biom_table= load_table(biom_file_path)

        
    def biom_to_count_dataframe(self):
        count_data= self.biom_table.matrix_data.toarray()
        sample_ids= self.biom_table.ids('sample')
        obs_ids= self.biom_table.ids('observation')
        
        return DataFrame(count_data, index= obs_ids, columns= sample_ids)


