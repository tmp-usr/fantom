
from selection import *
import metadata_worker
from storm.locals import *

database=create_database('sqlite:../../db/fantom.db')
store= Store(database)
md= metadata_worker.MetadataLoader(u'gut',store)
f= "/Users/kemal/phd/projects/fantom/albiorix/master/example_files/cog_table_metahit.tsv"
fm= FamReader(f)
dbh= DBHierarchy('cog',f, store)
gb= GroupBuilder(md, fm, dbh)
auto= CategoricalGroups(md,fm)
gb.addGroup()
gb.addGroup()
gb.addFilter(0, 'Age', 60, '>')
gb.addFilter(1, 'Age', 40, '<')
comp= Comparison(gb)
#comp.compare("mwu")
values= gb.groups[0].fam

# Run the program
a="""
if __name__ == "__main__":
    app = wx.App(False)
    frame = PlotPanel(None)
    
    frame.disp.plotHist(np.array(values), 100)
    frame.Show()
    app.MainLoop()
"""


