import pandas as pd
import numpy as np
from pdb import set_trace as bp

#######################################
##### DATAFRAME COLUMN PROCESSING #####
#######################################

def check_df_nans(df):
    
    return df.isnull().sum()

def check_df_duplicates(df):
    '''
    check duplicates columns in the dataframe
    '''
    return df.duplicated().sum()

def split_duplicates(series):
    '''
    return series_unduplicated, series_duplicated   
    '''
    duplicates = series.duplicated()
    series_unduplicated = series[~duplicates]
    series_duplicated = series[duplicates]

    return series_unduplicated, series_duplicated

def ts_split_duplicates_index(ts):
    '''
    return ts_undup, ts_dup
    split a time-series based on unduplicated and duplicated index
    '''
    
    #ts with no duplicates (keep first value of duplicated index elements)
    ts_undup = ts.loc[~ts.index.duplicated(),:]

    #ts with all the duplicates (including the ones in ts_undup and the ones excluded)
    ts_index_undup, ts_index_dup = split_duplicates(ts.index)
    ts_dup = ts.loc[ts_index_dup]

    return ts_undup, ts_dup

def ts_visual_index_duplicates(ts, c, ax, 
                               scatter_duplicates = 5):
    '''
    ts
    visual the duplicated values for a specific column
    '''

    assert pd.api.types.is_datetime64_any_dtype(ts.index), "Index must be a datetime index"

    ts_undup, ts_dup = ts_split_duplicates_index(ts)
    print(len(ts_undup), len(ts_dup))

    #ax = axes[0]
    ax.plot(ts_undup[c])
    ax.set_title('time-series')
    #ax = axes[1]
    #ax.set_xlim(axes[0].get_xlim())
    #ax.set_ylim(axes[0].get_ylim())

    ax.scatter(ts_dup[c].index, ts_dup[c], color='red', s=scatter_duplicates, zorder=3, label='duplicates')
    ax.legend()
    ax.set_title('scatter plot of duplicated points')



#####################################
##### TIME-SERIES PREPROCESSING #####
#####################################

def check_ts_gaps(ts, freq_seconds=3600, start=None):
    """
    ts : timeseries with datetime index
    return dataframe with left-right borders of temporal gaps
    start : expected start timestamp; if provided, a gap before the first entry is detected
    """

    _index = ts.index
    assert pd.api.types.is_datetime64_any_dtype(_index), "Index must be a datetime index"
    assert not _index.duplicated().any(), "Index must not contain duplicates"
    assert _index.is_monotonic_increasing, "Index must be sorted"


    index = _index.copy()
    series = pd.Series(index)
    diffs = series.diff()#.fillna(0)

    if freq_seconds is None:
        freq_seconds = diffs.min().total_seconds()

    #boolean vector indicating the right time-stamp of a gap
    bool_index_gap_end = diffs > pd.Timedelta(seconds=freq_seconds)

    #boolean vector including the left-right time-stamps of the gap
    bool_index_gap_start = bool_index_gap_end.shift(-1).fillna(False)

    print(len(bool_index_gap_end), len(bool_index_gap_start))

    g_end = ts.loc[bool_index_gap_end.values]
    g_start = ts.loc[bool_index_gap_start.values]

    ts_gaps = pd.concat([g_start.reset_index().add_suffix('_start'),
                         g_end.reset_index().add_suffix('_end')], 
                         axis=1)

    return ts_gaps



#[2] dataframe analysis
