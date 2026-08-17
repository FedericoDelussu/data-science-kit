import pandas as pd
import numpy as np
from pdb import set_trace as bp


############################################
##### PARSE FOLDER WITH MULTIPLE FILES #####
############################################

#FUNCTION ORIENTED CODE

def parse_folder_filesize(path_files):
    '''
    path_files: folder containing a collection of csv files  
    '''

    #list of file names
    files_names = [f.split('csv')[0] for f in os.listdir(path_files)]

    #list of file paths
    files_paths = [Path(f'{path_files}{f}') for f in os.listdir(path_files)]

    #list of file sizes in Mb 
    files_sizes = [f.stat().st_size/(1024*1024) for f in files_paths]

    return files_names, files_paths, files_sizes

def parse_folder_specs(path_files):
    '''
    give the specs of the files included in the folder
    '''
    files_names, files_paths, files_sizes = parse_folder_filesize(path_files)
    return dict(zip(files_names, files_sizes))

def parse_folder_datasets(path_files, nrows= None):
    '''
    read datasets contained in the folder
    '''
    files_names, files_paths, files_sizes = parse_folder_filesize(path_files)
    files = [pd.read_csv(f, nrows=nrows) for f in files_paths]
    return dict(zip(files_names, files))

#CLASS ORIENTED PROGRAM

class FolderParser:
    """
    Parse a folder, inspect file specs and optionally load datasets.
    """

    def __init__(self, folder):
        #attributes of the class
        self.folder = Path(folder)

        self.files = [
            f for f in self.folder.iterdir()
            if f.is_file()
        ]

        self.file_specs = self._get_file_specs()
        self.data = {}

    def _get_file_specs(self):
        """
        Return {filename: {"size_mb": ..., "format": ...}}
        """
        return {
            f.name: {
                "size_mb": f.stat().st_size / 1024**2,
                "format": f.suffix.lower()
            }
            for f in self.files
        }

    def load_data(self, nrows=None, csv_only=True):
        """
        Load files into self.data.

        Parameters
        ----------
        nrows : int or None
            Number of rows to read.
        csv_only : bool
            If True, load only CSV files.
        """

        files_to_load = self.files

        if csv_only:
            files_to_load = [
                f for f in self.files
                if f.suffix.lower() == ".csv"
            ]

        self.data = {
            f.stem: pd.read_csv(f, nrows=nrows)
            for f in files_to_load
        }

        return self.data


#######################################
##### DATAFRAME EXPLORATION #####
#######################################

def check_df_nans(df):
    
    return df.isnull().sum()

def check_nan_entries(df_ag, column):
    '''
    count total records and records without assigned locations
    '''
    lambda_get_df_nans = lambda df : df[df[column].isna()]

    df_agn = lambda_get_df_nans(df_ag)
    print(f'total records {len(df_ag)}')
    print(f'nan location records {len(df_agn)}')

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
