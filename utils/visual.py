from Modules.sankey import sankey

def sankey_df(df, colorDict, ax=None):
    sankey(df['true'],
           df['predicted'],
           aspect=20,
           colorDict=colorDict,
           fontsize=12,
           ax=ax)

#correlation of the dataframe
def corr_df(corr, 
            ax=None, 
            cmap="RdYlGn", 
            vmin=-1, 
            vmax=1, 
            **kwargs):
    '''
    corr eg. input_df.corr()
    '''
    if ax is None:
        plt.figure(figsize=(15,12))
    #plot heat map
    g=sns.heatmap(corr, annot=True, cmap=cmap, vmin=vmin, vmax=vmax, ax=ax, **kwargs)
    (ax if ax is not None else plt.gca()).set_title('Feature Correlation')

    if ax is None:
        return plt.show()