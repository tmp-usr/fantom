from balter.balter import Balter

from fantom.src.helper.file_provider import FileProvider
from hierarchy_provider import HierarchyProvider


db_name = "kegg_orthology"
file_provider= FileProvider('periphyton',db_name)
file_path= "/Users/kemal/tmp/pp_kegg_short.tsv"

def test_file_provider():
    print file_provider['example']['abundance']

def test_balter():
    b= Balter(db_name,'/Users/kemal/repos/dev/balter/data/balter.db')
    print b

def test_hierarchy_provider():
    b= Balter(db_name,'/Users/kemal/repos/dev/balter/data/balter.db')
    hp= HierarchyProvider(file_provider, b, file_path)
    #hp.get_abundance_by_level(2)

def test_hierarchy_abundance_by_level():
    b= Balter(db_name,'/Users/kemal/repos/dev/balter/data/balter.db')
    hp= HierarchyProvider(file_provider, b, file_path)
    print hp.get_abundance_by_level(2)

def test_hierarchy_abundance_by_level_category():
    b= Balter(db_name,'/Users/kemal/repos/dev/balter/data/balter.db')
    hp= HierarchyProvider(file_provider, b, file_path)
    print hp.get_abundance_by_level_category(2,"a")


#test_file_provider()
#test_balter()
#test_hierarchy_provider()
test_hierarchy_abundance_by_level_category()
