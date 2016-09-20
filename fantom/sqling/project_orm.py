from storm.locals import Unicode, Int, Float, Reference


class ProjectORM(object):
    __storm_table__='project'
    id=Int(primary=True)
    name=Unicode()
    metadata_path=Unicode()

class SampleORM(object):
    __storm_table__='sample'
    id=Int(primary=True)
    name=Unicode()
    project_id=Int()
    project=Reference(project_id,ProjectORM.id)
        

class MetadataORM(object):
    __storm_table__='metadata'
    id=Int(primary=True)
    name=Unicode()
    data_type=Int()
    project_id=Int()


class MetadataValueORM(object):
    __storm_table__='metadata_value'
    id=Int(primary=True)
    string_value=Unicode()
    int_value=Int()
    float_value=Float()
    metadata_id=Int()
    metadata=Reference(metadata_id, MetadataORM.id)


class SampleMetadataORM(object):
   __storm_table__= 'sample_metadata'  
   __storm_primary__= 'sample_id', 'metadata_value_id'
   sample_id=Int() 
   metadata_value_id = Int()


