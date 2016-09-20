import os

base_dir= os.path.join(os.getcwd())  

class FileProvider(dict):
    """
        abundance file name format: project.db.level.transformation.tsv

    """

    def __init__(self, project_name, db_name, *args, **kwargs):
        
        self.update(*args, **kwargs)

        self.project_name= project_name
        self.db_name= db_name
        
        self.dirs= {
            
            'config': dict.fromkeys(['log','settings'],''),

            'tmp': dict.fromkeys(['plots','tables'], ''),
                
            'data': dict.fromkeys(['db', 'abundance', 'abundance_with_enzymes', 'metadata'], ''),
            
            'example': dict.fromkeys(['abundance', 'metadata'], ''),

            'output': dict.fromkeys(['plots', 'tables', 'report'], '')
                
            }
        
        self.paths= self.dirs.copy()
        
        self.makedirnames()
        self.makedirs()
        self.paths['config']['log']= os.path.join(self.dirs['config']['log'],'%s.%s.log' %(self.project_name, self.db_name))

        self.paths['config']['setting']=  os.path.join(self.dirs['config']['settings'], '%s.%s.config' %(self.project_name, self.db_name))


        self.paths['data']['db']=  os.path.join(self.dirs['data']['db'], 'fantom.db')
        self.paths['data']['metadata']= os.path.join(self.dirs['data']['metadata'], '%s.tsv' % self.project_name)
        self.paths['data']['abundance']= os.path.join(self.dirs['data']['abundance'], '%s.%s' %(self.project_name, self.db_name))
        self.paths['data']['abundance_with_enzymes']= os.path.join(self.dirs['data']['abundance_with_enzymes'], '%s.%s.%s' %(self.project_name, self.db_name, 'with_enzymes'))

        
        self.paths['example']['abundance']= os.path.join(self.dirs['example']['abundance'], '%s.%s.tsv' %(self.project_name, self.db_name ))
        self.paths['example']['metadata']= os.path.join(self.dirs['example']['metadata'], '%s.%s.tsv' %(self.project_name, "metadata"))

        self.paths['output']['report']= os.path.join(self.paths['output']['report'], '%s.%s.pdf' % (self.project_name, self.db_name) )


    def __getitem__(self, item):
        return self.paths.__getitem__(item)
    
    def get_dir(self, item):
        return self.dirs[item]


    def makedirnames(self):
        file_dir= os.path.join(base_dir, '.files')
        #if os.path.basename(base_dir) == 'fantom':
        for dir1,v in self.dirs.iteritems():
                for dir2, path in v.iteritems():
                    if dir1 == "data" and dir2.startswith('abundance'):
                        #if not os.path.exists(dir2_value): os.makedirs(dir2_value)
            
                        project_db_dir= os.path.join(file_dir, dir1, dir2, self.project_name, self.db_name)
                        self.dirs[dir1][dir2]= project_db_dir

                    else:
                        #if not os.path.exists(self.project_db_dir): os.makedirs(self.project_db_dir)
                        dir2_value= os.path.join(file_dir, dir1, dir2)
                        self.dirs[dir1][dir2]= dir2_value

    def makedirs(self):
        if os.path.basename(base_dir) == 'fantom':
            for dir1,v in self.dirs.iteritems():
                for dir2, path in v.iteritems():
                    if not os.path.exists(self.dirs[dir1][dir2]): os.makedirs(self.dirs[dir1][dir2])

    

    def get_abundance_file_by_level(self, level= 1, transformation="relative"):
        return '%s.%s.%s.tsv' %(self.paths['data']['abundance'], level, transformation) 

    def exists(self, path):
        return os.path.exists(path)
    
#fp= FileProvider('periphyton','kegg')    
#print fp.get_abundance_file_by_level('main')

