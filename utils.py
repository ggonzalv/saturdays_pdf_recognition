import os,sys
from pdf2image import convert_from_path
from tqdm import tqdm

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
# Read files in directory
# ---------------------------------------------------------------

def read_files(inputDir: str, nFiles=-1):
    '''
    Read all files in directory and convert it to raw text
    input:
        inputDir: name of input directory (str)
        nFiles: number of files to read (int, optional)
    '''
    images = []
    i = 0
    for file in tqdm(os.listdir(inputDir), desc="Processing files"):
        if i == nFiles:
            break
        tFile = f"{inputDir}/{file}"
        if check_file(tFile):
            images.extend(readPDF(tFile))
        i += 1
    return images

# ---------------------------------------------------------------
# Read PDF file and convert it to string
# ---------------------------------------------------------------
def readPDF(tFile: str, npages=-1):
    '''
    Read PDF file and convert it to images
    input:
        tFile: name of the file (str)
        pages: number of pages to read (int, optional)
    output:
        images: list of images (list)
    '''
    fName = tFile.split("/")[-1].split('.')[0]
    # Create output directory if not exist
    createDir(f"images/{fName}")
    # convert pdf to images
    if npages == -1:
        images = convert_from_path(tFile, dpi=300, fmt="png", output_folder=f'images/{fName}', output_file=f"{fName}_")
    else:
        images = convert_from_path(tFile, dpi=300,first_page=1, last_page=npages,fmt="png", output_folder=f'images/{fName}', output_file=f"{fName}_")

    return images

# ---------------------------------------------------------------
# Create Directory if NOT exists
# ---------------------------------------------------------------
def createDir(directory: str):
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
                print(f"{bcolors.FAIL}Error: Directory {directory} cannot be created!{bcolors.ENDC}")
                sys.exit()

# ---------------------------------------------------------------
# Check if file exists and is in proper format
# ---------------------------------------------------------------
def check_file(tFile: str):
    '''
    Check if file exists and is in proper format
    input:
        tFile: name of the file (str)
    output:
        True: if file exists and is in proper format
    '''
    if not os.path.isfile(tFile):
        print(f"{bcolors.FAIL}ERROR: File {tFile}  does not exist!{bcolors.ENDC}")
        return False
    if not tFile.endswith(".pdf"):
        print(f"{bcolors.FAIL}ERROR: File {tFile} is not a valid pdf file! {bcolors.ENDC}")
        return False
    return True

# ---------------------------------------------------------------
# Check if directory exists
# ---------------------------------------------------------------
def check_dir(inputDir: str):
    '''
    Check if directory exists
    input:
        inputDir: name of the directory (str)
    output:
        True: if directory exists
    '''
    if not os.path.isdir(inputDir):
        print(f"{bcolors.FAIL}ERROR: Directory {inputDir}  does not exist!{bcolors.ENDC}")
        return False
    return True