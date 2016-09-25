from project_orm import ProjectORM, SampleORM, SampleMetadataORM, MetadataValueORM, MetadataORM

class ProjectBase(object):
    def __init__(self, project_name, store):
        self.project_name= unicode(project_name)
        self.store = store
        
        project_orm= self.store.find(ProjectORM, ProjectORM.name == self.project_name).one()
        
        if not project_orm:
            self.exists= False

        else:
            self.exists= True
            self.project_orm= project_orm
        
    
    def delete_metadata(self):
        samples= self.store.find(SampleORM, SampleORM.project_id == self.project_orm.id)

        for sample in samples:
            sample_metadatas= self.store.find(SampleMetadataORM, SampleMetadataORM.sample_id == sample.id)
            for sample_metadata in sample_metadatas:
                metadata_value= self.store.find(MetadataValueORM, MetadataValueORM.id == sample_metadata.metadata_value_id).one()
                if metadata_value:
                    self.store.remove(metadata_value)
                    self.store.remove(sample_metadata)
            
            self.store.remove(sample)
        self.store.remove(self.project_orm)
        self.store.commit()


