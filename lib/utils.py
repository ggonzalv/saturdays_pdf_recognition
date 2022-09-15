import os
import sys
import shutil
import gzip
import pandas as pd


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ---------------------------------------------------------------
# Create Directory if NOT exists
# ---------------------------------------------------------------


def createDir(directory: str, clean: bool = False):
    '''
    Create directory if not exists

    input:
        directory: name of directory (str)
    '''
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            if os.path.islink(directory):
                os.remove(directory)
                os.makedirs(directory)
            else:
                print(
                    f"{bcolors.FAIL}Error: Directory {directory} cannot be created!{bcolors.ENDC}")
                sys.exit()
    elif clean:
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))

# ---------------------------------------------------------------
# Read Configuration File
# ---------------------------------------------------------------


def readConfig(configFile, verbose=False):
    '''
    Read configuration file parameters

    input:
        configFile: name of the configuration file (str)
        verbose: additional prints for debugging (bool)
    output:
        parameters: dictionary of read parameters (dict)
    '''
    parameters = {}

    try:
        with open(configFile, 'r') as InputFile:
            while 1:
                line = InputFile.readline()
                if not line:
                    break
                if '#' not in line and len(line) > 1:
                    command = line.split("=")
                    parameters[command[0].strip()] = eval(command[1].strip())

        if verbose:
            print(
                f"{bcolors.OKBLUE}Configuration parameters: {parameters}{bcolors.ENDC}")
        return parameters
    except IOError:
        print(f"File {configFile} does not exist!")
        sys.exit()


# ---------------------------------------------------------------
# Clean empty pieces of text in dataframe
# ---------------------------------------------------------------
def clean_df(df: pd.DataFrame):
    '''
    Clean dataframe

    input:
        df: dataframe with pytesseract image_to_data output (pd.DataFrame)

    output:
        df: dataframe without empty pieces of text (pd.DataFrame)
    '''
    # Keep only blocks with text and with reliable confidence
    # Get only high quality data
    df = df[(df.conf.astype(float) > 10) & (df.text != ' ') & (df.text != '')]
    df = df[['par_num', 'line_num', 'word_num', 'left',
             'top', 'width', 'height', 'conf', 'text']]
    df.reset_index(drop=True, inplace=True)
    # df.to_csv("test.csv")
    if len(df['par_num'].unique()) > 1:
        columnLabeler = ColumnLabeler()
        df['line_num'] = df.apply(lambda x: columnLabeler.set_lines(x), axis=1)
    df.drop("par_num", axis=1, inplace=True)
    return df

# ---------------------------------------------------------------
# Preserve indentation using image_to_data and pandas
# ---------------------------------------------------------------


def get_columns(df: pd.DataFrame):
    '''
    Get columns for each piece of text 

    input:
        df: dataframe with OCR text (pd.DataFrame)

    output:
        df: dataframe with additional col_num column (str)
    '''
    grouped_df = df.groupby(['line_num'])
    lines = list(grouped_df.groups.keys())
    df_line = []
    for line in lines:
        sub_df = grouped_df.get_group(line)
        sub_df.reset_index(drop=True, inplace=True)
        # Indent text
        sub_df_copy = sub_df.copy()
        columnLabeler = ColumnLabeler()
        sub_df_copy['col_num'] = sub_df.apply(
            lambda x: columnLabeler.get_column(x), axis=1)
        df_line.append(sub_df_copy)
    df = pd.concat(df_line)
    df = df.groupby(['line_num', 'col_num'])[
        'text'].apply(lambda x: ' '.join(x))

    return df


class ColumnLabeler:
    '''
    Simple class to extract column for each piece of text
    '''

    def __init__(self):
        self.prev_par = 1
        self.prev_line = 1
        self.correct_line = 1
        self.prev_left = 0
        self.prev_width = 0
        self.col_num = 1
        self.isFirst = True

    def get_column(self, x):
        '''
        Insert indeces in line
        '''
        if self.isFirst:
            self.prev_left = x['left']
            self.prev_width = x['width']
            self.isFirst = False
            return self.col_num
        if x['left'] - (self.prev_left + self.prev_width) > 20:
            self.col_num += 1
        self.prev_left = x['left']
        self.prev_width = x['width']
        return self.col_num

    def set_lines(self, x):
        """
        Set lines for column labeler
        """
        if x['par_num'] != self.prev_par or x['line_num'] != self.prev_line:
            self.prev_par = x['par_num']
            self.prev_line = x['line_num']
            self.correct_line += 1
        return self.correct_line

# ------------------------------------------------------------
# Compress output file to zip file
# ------------------------------------------------------------


def compressOutput(file_path: str, verbose: bool = False):
    '''
    Compress output file to zip file
    input:
        file_path: name of the output file (str)
        verbose: additional prints for debugging (bool, optional)
    '''
    if verbose:
        print(f"{bcolors.OKBLUE}Compressing output file into zip format{bcolors.ENDC}")
    shutil.make_archive(file_path.replace(".pdf", ""), 'zip', '/tmp/test-api/tmp_output_files')


# ------------------------------------------------------------
# Clean directories used during execution
# ------------------------------------------------------------


def cleanDirectories():
    '''
    Clean directories used during execution
    '''
    shutil.rmtree('/tmp/test-api/images')
    shutil.rmtree('/tmp/test-api/tmp_output_files')
