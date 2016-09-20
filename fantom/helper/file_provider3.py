import os, sys

base_dir= os.path.join(os.getcwd())  
data_dir= os.path.join(base_dir, 'data')

project_sql_db_path=""


class FileProvider(dict):
    
    def __init__(self, project_name, *args, **kwargs):
        self.update(*args, **kwargs)
        self._dict= dict()
        self.project_name= project_name
        
        self.tmp_dir=  os.path.join(data_dir, project_name, 'tmp')
        self.example_dir= os.path.join(data_dir, 'example')
        self.icon_dir= os.path.join(data_dir, 'icons')
        self.output_dir= os.path.join(base_dir, 'outputs')
        
        enz_types= ["with_enzymes","without_enzymes"]
        norms= ["relative","absolute"]
        
        

        #self._dict['config'] = {
        
        #}

        self._dict['tmp'] = {
            # since hierarchy levels will differ from db to db, we should find an expandable solution
            # for the file names. for now, lets keep the config type as a dir and get the file from a function
            # below
            'plots' : os.path.join(self.tmp_dir, "plots"),  
            'tables': os.path.join(self.tmp_dir, "tables"), 
             
            }        
        
        self._dict['output']= {
            'plots': os.path.join( output_dir, "plots"), 
            'tables': os.path.join( output_dir, "tables"), 
            } 
        
        self._dict['example']=  {
            'kegg': os.path.join(example_dir, "periphyton_kegg.tsv"),

            'metadata': os.path.join(example_dir, "periphyton_metadata.tsv")
            }


        self.makedirs()

    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def abundance(self, project_name, db_name):
        self._dict['tmp']['abundance']= os.path.join(self['tmp']['tables'], '%s.fam.hier' % (db_name))
        return self._dict['tmp']['abundance']

    def abundance_by_level(self, level, with_enzymes=False):

   


    def makedirs(self):
        for cat, label_path in self._dict.iteritems():
            for label, path in label_path.iteritems(): 
                if os.path.isfile(path):
                    path = os.path.dirname(path)

                if not os.path.exists(path):
                    if os.path.basename(os.path.dirname(path)) == "fantom":        
                        os.makedirs(path)

