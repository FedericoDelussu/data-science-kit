from Modules.sankey import sankey

def sankey_df(df, colorDict, ax=None):
    sankey(df['true'],
           df['predicted'],
           aspect=20,
           colorDict=colorDict,
           fontsize=12,
           ax=ax)