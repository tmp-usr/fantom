from pandas import DataFrame, Panel, MultiIndex


def basicToMultiIndex(df, nLevels):
    df= df.copy()
    level_names=df.columns[:nLevels+1]
    index_tuples= [i[1:] for i in df[level_names].itertuples()]
    index= MultiIndex.from_tuples(index_tuples, names= level_names )
    df.index= index
    df=df.drop(level_names, axis=1)
    return df


def basicToPanel(df, nLevels):
    df= df.copy()
    
    #df_hier= df[df.columns[-nLevels-1:]]
    #df_counts= df[df.columns[:-nLevels-1]]
    #
   
    df_counts= df[df.columns[nLevels+1:]]
    df_hier= df[df.columns[:nLevels+1]]
   

    pnl_fam= Panel({'db':df_hier, 'counts':df_counts})
    return pnl_fam


def panelToBasic(pnl):
    return DataFrame(pnl['db'].dropna(axis=1).join(pnl['counts'].dropna(axis=1)))


def panelToMultiIndex(pnl):
    """ Something wrong! Get back later!!! """ 
    pnl = pnl.copy()
    level_names= pnl['db'].columns
    index_tuples= [i[1:] for i in pnl['db'].itertuples()]
    index= MultiIndex.from_tuples(index_tuples, names= level_names )
    df= pnl['counts']
    df.set_index(index)
    return df


def multiIndexToPanel(df, nLevels):
    df = df.copy()
    df1= DataFrame(df.index.tolist(), columns= df.index.names)
    df.index= range(len(df.index))
    df2=df
    pnl_fam= Panel({'db':df1, 'counts':df2})
    return pnl_fam



def multiIndexToBasic(df, nLevels):
    df= df.copy()
    df1= DataFrame(df.index.tolist(), columns= df.index.names)
    df.index= range(len(df.index))
    df2=df
    return df1.join(df2)




