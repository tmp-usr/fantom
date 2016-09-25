from pandas import read_csv

from pandas_data_types import *

df= read_csv('unnamed.cog.heier', sep= "\t", index_col="Name")
#= read_csv('/Users/kemal/repos/fantom/fantom/data/example/periphyton_kegg.tsv', sep= "\t", index_col="Name")
