from openpyxl import load_workbook



from fantom.sqling.project_orm import MetadataORM, EnvPackageORM, EnvPackageMetadataORM


create_table_strings= {"create_project_string": """CREATE TABLE project (id INTEGER PRIMARY KEY, 
                                             name VARCHAR)
                       """,


"create_sample_string": """CREATE TABLE sample (id INTEGER PRIMARY KEY, 
                                           name VARCHAR UNIQUE, 
                                           project_id INTEGER,  
                                           FOREIGN KEY(project_id) 
                                           REFERENCES project(id) ON DELETE CASCADE)
                      """,

"create_metadata_string": """CREATE TABLE metadata (id INTEGER PRIMARY KEY, 
                                               name VARCHAR, 
                                               mandatory INTEGER,
                                               data_type INTEGER 
                                               )
                        """,

"create_env_package_string": """CREATE TABLE env_package (id INTEGER PRIMARY KEY, 
                                               name VARCHAR)
                        """,

"create_env_package_metadata_string": """CREATE TABLE env_package_metadata (metadata_id INTEGER, 
                                                            env_package_id INTEGER, 
                                                            PRIMARY KEY (metadata_id, env_package_id))

""",

"create_metadata_value_string": """CREATE TABLE metadata_value (id INTEGER PRIMARY KEY, 
                                                          string_value VARCHAR, 
                                                          int_value INTEGER, 
                                                          float_value FLOAT, 
                                                          metadata_id INTEGER, 
                                                          FOREIGN KEY (metadata_id) 
                                                          REFERENCES metadata(id) ON DELETE CASCADE)
                             """, 

"create_sample_metadata_string": """CREATE TABLE sample_metadata (sample_id INTEGER, 
                                                            metadata_value_id INTEGER, 
                                                            PRIMARY KEY (sample_id, metadata_value_id))

                               """
                               }

class MetadataSelector(object):
    def __init__(self, store):
        self.store = store

    def get_metadata_by_name(self, name):
        return self.store.find(MetadataORM, MetadataORM.name == name).one()

    def get_env_package_by_name(self, name):
        return self.store.find(EnvPackageORM, EnvPackageORM.name == name).one()

    def get_metadata_names(self):
        return self.store.find(MetadataORM).all()

    def get_env_package_names(self):
        return self.store.find(EnvPackageORM).all()

    


class MetadataInserter(object):
    def __init__(self, store):
        self.store= store
        
        self.mandatory_metadata=map(str.lower, ["latitude","longitude","country","location","collection_date","collection_time","collection_timezone","biome","feature","material","env_package"])
        
        self.table_names= ["project", "sample", "metadata", "metadata_value", "sample_metadata", "env_package", "env_package_metadata"]
        
        table_list= [table[0] for table in self.store.execute('select tbl_name from SQLITE_MASTER')]

        if set(table_list).intersection(set(self.table_names)) != set(self.table_names):
            self.drop_tables()
            self.create_tables()

            
    def create_tables(self): 
        for k,v in create_table_strings.iteritems():
            self.store.execute(v)
        self.store.commit()


    def drop_tables(self):
        drop_table_strings= ["drop table %s" %table_name for table_name in self.table_names]
        for v in drop_table_strings:
            self.store.execute(v)
        self.store.commit()


    def insert_from_mixs_template(self, mixs_template):
        self.workbook= load_workbook(excel_file)
        self.sheet_names= self.workbook.get_sheet_names()
        for sheet_name in self.sheet_names:
            if sheet_name.startswith("ep"):
                env_package_name= sheet_name.lstrip("ep_")
                
                ep= EnvPackageORM()
                ep.name= env_package_name
                self.store.add(ep)

                sheet= self.workbook.get_sheet_by_name(sheet_name)
                
                row1= list(sheet.rows)[0]
                row2= list(sheet.rows)[1]

                row1_entries= [c.value for c in row1][1:]
                
                for entry in row1_entries:
                    md= self.store.find(MetadataORM, MetadataORM.name == entry).one()
                    if md is None:
                        md= MetadataORM()
                        md.name= entry
                        if entry.lower() in self.mandatory:
                            md.mandatory = True
                        self.store.add(md)
                        
                    epm= EnvPackageMetadataORM()
                    epm.metadata_id= md.id
                    epm.env_package_id= ep.id
                    self.store.add(epm)
        
            
        self.store.commit()


fantomii_db= "fantomii.db"
excel_file= "/Users/kemal/Desktop/mgrast_mixs_template.xlsx"

from storm.locals import create_database, Store

fantom_sqlite_db = create_database("sqlite:%s" % fantomii_db )
store= Store(fantom_sqlite_db)

mi= MetadataInserter(store)
mi.insert_from_mixs_template(excel_file)


