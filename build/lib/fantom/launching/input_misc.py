class InputBase(object):
    def __init__(self, path, loca= True):
        self.path = path
        self.local= local

class SeqDataInput(InputBase):
    def __init__(self, db_name, project_id):
        self.db_name = db_name
        self.project_id = project_id

class CountInput(SeqDataInput):
    def __init__(self):
        pass

class TabularBlastInput(SeqDataInput):
    def __init__(self, e_value, percent_id, overlap):
        self.e_value = e_value
        self.percent_id = percent_id
        self.overlap = overlap
