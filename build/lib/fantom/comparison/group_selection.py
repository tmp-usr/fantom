from pandas import DataFrame, Series, read_csv
from fantom.src.project.project import Sample, Metadata
#from analyzer import *

#from storm.locals import *
#import metadata_worker

#from dbhierarchy import *


        
class Group(object):
    """
        md: metadata_worker
        fm: feat
    """

    def __init__(self, project):
        self.log= []
        self.project= project
        self.data= self.project.data
        #self.fm= fm
        self.name= "" 
        self.color=(0,0,255,255)
        #self.sample_names= [sample.name for sample in self.project.get_all_samples()]
        #self.samples= self.initial_samples= [Sample(sample_name, Metadata(metadata)) for (sample_name, metadata) in 
        #        [(sample_name, self.md.getSampleMetadata(sample_name)) for sample_name in self.sample_names]]   
        #self.abundance_frame= abundance_frame
        self.samples= self.project.get_samples()
        #self.data= abundance_frame[self.names]
        self.trash=[]

    def __str__(self):return str(self.log) if self.name is "" else self.name
    def __len__(self):return len(self.samples)
    def __repr__(self):return '; '.join(self.names)
    
    @property
    def names(self): return [s.name for s in self.samples]

    def get_name(self):return self.name
    def set_name(self, name):self.name= name

    def get_color(self):return self.color
    def set_color(self, color):self.color=color

    def get_metadata(self, category):
        return Series({s.name: s.metadata[category] for s in self.samples})

    def add_filter(self, prop, value, operator):
        if (prop, value, operator) in self.log:
            print 'already selected'
            return
        self.log.append((prop,value,operator))
        
        samples= [sample for sample in 
                self.project.get_samples_by_prop(prop, value, operator)]
            
        self.trash.append(tuple(set(
            self.samples).difference(
            set(samples))))
        
        self.samples= list(set(
            samples).intersection(
            set(self.samples)))
        
        #import pdb
        #pdb.set_trace()
        self.data.select([sample.name for sample in self.samples])
    #def get_data(self):
    #    self.data.select(self.names)


    def set_level(self, level):
        self.data.set_level(level)    

    def undo(self):
        self.undo_log=self.log.pop()
        self.samples+= self.trash.pop()

        self.data.select(self.names)
   

    def redo(self):
        self.add_filter(*self.undo_log)
        self.undo_log= None

    def to_transformed(self):
        self.data.to_transformed()
    
    def to_absolute(self):
        self.data.to_absolute()


class GroupContainer(object):
    
    def __init__(self, name= ""):#, db_hierarchy):
        '''
        Args:
            md: metadata_worker object instance : replaced with project
            fm: feature abundance dataframe : abundance_frame
            dh: dbhierarchy object instance : db_hierarchy
        '''
        #self.project = project
        #self.abundance_frame= abundance_frame
        self.name= name
        #self.db_hierarchy= db_hierarchy
        self.groups=[]
        self.auto_groups= None
        #self.add()

    def __len__(self): return len(self.groups)
    def __str__(self): return self.name 
    def __repr__(self): return self.name 
    def __iter__(self): return self.groups.__iter__()
    def __getitem__(self, index): return  self.groups[index]

    def get_current_group(self):return self.current_group


    def add(self, project):
        group= Group(project)
        self.groups.append(group)
        self.current_group= self.groups[-1]
        return group

    def get_data_frames(self):
        return [group.data.data_frame for group in self.groups]

    def add_filter(self, prop, value, operator):
        '''
            criteria are prop,value, operator respectively
        '''
        self.current_group.add_filter(prop, value, operator)
  

    def get_selected_metadata(self,  prop ):
        metadata= set([str(s.metadata[prop]) for s in self.group.samples])
        return metadata    

    def undo(self):
        self.current_group.undo()

    def redo(self):
        self.current_group.redo()

    def set_group_name(self, name):
        self.current_group.set_name(name)
    
    def set_group_color(self, color):
        self.current_group.set_color(color)
    
    #@property  #  memoize this property  
    #def means(self):
    #    return [group.abundance_frame.T.mean().order(ascending=False) for group in self.groups]
    
    #@property  #  memoize this property
    #def stds(self):
    #    return [group.abundance_frame.T.std().order(ascending=False) for group in self.groups]

    #def select_by_db_level(self, level):
    #    dfMain= self.project.select_by_level(level)
    #    for group in self.groups:
    #        group.fam= dfMain[group.fam.columns]
    
    
    #def set_db_hierarchy_level(self, level):
    #    self.project.set_db_hierrchy_level(level)

    def to_transformed(self):
    #    self.project.data.to_relative()
        
        for group in self.groups:
            group.to_transformed()

    def to_absolute(self):
        #self.project.data.to_absolute()
        for group in self.groups:
            group.to_absolute()
    
    def set_db_hierarchy_level(self, level):
        for group in self.groups:
            group.set_level(level)

    def get_metadata(self, category):
        metadata= Series()
        for group in self.groups:
            metadata=metadata.append(group.get_metadata(category))
        return metadata


a="""

    
    def auto_select_categorical(self):
        "\""
            returns a dictionary of group container objects 
        "\""
        auto_groups= {}
        
        category_values= self.project.get_categorical_samples()
        for category, value_samples in category_values.iteritems():
            container= GroupContainer(self.project, self.abundance_frame, name= category )
            for value, samples in value_samples.iteritems():
                container.add()
                container.add_filter(category, value ,'=')
            auto_groups[category]= container    
        return auto_groups

    
    def reindex_sorted(self, reverse=False):
        newIndex= self.means[0].index
        for group in self.groups:
            if reverse:
                group.abundance_frame= group.abundance_frame.reindex(reversed(newIndex))
            group.abundance_frame= group.abundance_frame.reindex(newIndex)
        

"""
