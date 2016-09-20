from fantom.src.sqling.project_selector import ProjectSelector
from fantom.src.project.project import Project
from fantom.src.comparison.group_selection import GroupContainer
from fantom.src.launching.dbhierarchy import DBHierarchy


from storm.locals import create_database, Store
from pandas import read_csv

data_frame= read_csv('../../data/kegg.tsv', index_col="Name", sep="\t")

sql_db_path= "/Users/kemal/dbs/fantom_db/fantom.db" 
db= create_database("sqlite:"+sql_db_path)
store= Store(db)

project_name= u"periphyton"

#ps= ProjectSelector(project_name, store)
dbh= DBHierarchy('kegg_orthology', data_frame, store, project_name= project_name)

dbh.select_by_level(2)

#project= Project(project_name, ps)

#print project.metadata_to_tsv('a.tsv')


#gc= GroupContainer(project, data_frame)

#auto_groups= gc.auto_select_categorical()


#gc.add_filter('PICT', 5.00 , '>')

#gc.add()
#gc.add_filter('irgarol', 'high' , '=')

#print repr(gc.groups[0])

#gc.get_current_group().samples

#gc.add_filter('PICT', '>', '0.05')

#gc.add()
#gc.add_filter('irgarol', 'very low', 'contains')
#print gc.groups[0].samples

#for sample in project.samples:
#    print sample.metadata['PICT']

