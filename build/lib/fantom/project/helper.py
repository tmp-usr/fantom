from storm.locals import create_database, Store

create_project_string= """CREATE TABLE project (id INTEGER PRIMARY KEY, 
                                             name VARCHAR, 
                                             metadataPath VARCHAR)
                       """

create_sample_string= """CREATE TABLE sample (id INTEGER PRIMARY KEY, 
                                           name VARCHAR UNIQUE, 
                                           projectID INTEGER,  
                                           FOREIGN KEY(projectID) 
                                           REFERENCES project(id) ON DELETE CASCADE)
                      """

create_metadata_string= """CREATE TABLE metadata (id INTEGER PRIMARY KEY, 
                                               name VARCHAR, 
                                               dataType INTEGER, 
                                               projectID INTEGER)
                        """

create_metadata_value_string= """CREATE TABLE metadata_value (id INTEGER PRIMARY KEY, 
                                                          string_value VARCHAR, 
                                                          int_value INTEGER, 
                                                          float_value FLOAT, 
                                                          metadataID INTEGER, 
                                                          FOREIGN KEY (metadataID) 
                                                          REFERENCES metadata(id) ON DELETE CASCADE)
                             """ 

create_sample_metadata_string= """CREATE TABLE sample_metadata (sampleID INTEGER, 
                                                            metadataValueID INTEGER, 
                                                            PRIMARY KEY (sampleID, metadataValueID))

                               """

def createProjectTables():
    database=create_database('sqlite:../../db/fantom.db')
    store=Store(database)
    store.execute(create_project_string)
    store.execute(create_sample_string)
    store.execute(create_metadata_string)
    store.execute(create_metadata_value_string)
    store.execute(create_sample_metadata_string)
    store.commit()

def dropProjectTables():
    database=create_database('sqlite:../../db/fantom.db')
    store=Store(database)
    store.execute('drop table project')
    store.execute('drop table sample')
    store.execute('drop table metadata')
    store.execute('drop table metadata_value')
    store.execute('drop table sample_metadata')
    store.commit()


