from balter import Balter
from fantom.src.helper.file_provider import FileProvider

path_to_balterdb=  '/Users/kemal/repos/balter/data/balter.db'


class iData(object):
    def __init__(self, db_name, file_path):
        
        self.balter= Balter(db_name, path_to_balterdb)

        self.hierarchy=  HierarchicalAbundanceData( balter, file_provider, file_path)
        self.hierarhcy.build_hierarchy_levels()
        self.current_data= self.hierarchy.get_abundance_by_level(self.biodb.get_level_count())

    
    def get_level_data(self, level):
        self.current_data= self.hierarchy.get_abundance_by_level(level)
        return self.current_data

    def to_relative(self):
        self.current_data.relative()
        return self.current_data

    def to_absolute(self):
        self.current_data.absolute()
        return self.current_data


file_path= '/Users/kemal/repos/fantom/.files/example/abundance/' + file_provider['example']['abundance']



