from pdf2image import convert_from_path
from tqdm import tqdm

from lib.utils import *

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
        print(
            f"{bcolors.FAIL}ERROR: File {tFile} is not a valid pdf file! {bcolors.ENDC}")
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
        print(
            f"{bcolors.FAIL}ERROR: Directory {inputDir}  does not exist!{bcolors.ENDC}")
        return False
    return True

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
    # convert pdf to images
    if npages == -1:
        images = convert_from_path(
            tFile, dpi=300, fmt="png", output_folder='/tmp/test-api/images', output_file=f"{fName}_")
    else:
        images = convert_from_path(tFile, dpi=300, first_page=1, last_page=npages,
                                   fmt="png", output_folder='/tmp/test-api/images', output_file=f"{fName}_")

    return images

# ---------------------------------------------------------------
# Read data files and extract images from them
# ---------------------------------------------------------------


def read_data(params: dict, verbose: bool = False):
    '''
    Read data files and extract images from them
    input:
        params: dictionary of parameters (dict)
        verbose: additional prints for debugging (bool)
    output:
        images: list of images (list)
    '''

    createDir("training_images")
    print(f"{bcolors.OKGREEN}Output dir {bcolors.ENDC}{bcolors.OKBLUE}training_images/{bcolors.ENDC}{bcolors.OKGREEN} created successfully!{bcolors.ENDC}")

    # For tests only. Read just one file
    if params['tFile']:
        # check if input file exists and is proper format
        if check_file(params['tFile']):
            print(
                f"{bcolors.OKGREEN}Reading {params['tFile']} and extracting images...{bcolors.ENDC}")
            # read file and convert it to images
            images = readPDF(params['tFile'], params['nPages'])

    elif params['inputDir']:
        # check if input directory exists
        if check_dir(params['inputDir']):
            print(
                f"{bcolors.OKGREEN}Reading all files in {params['inputDir']} and extracting images...{bcolors.ENDC}")
            # Read all files in directory
            images = read_files(params['inputDir'], params['nFiles'])

    return images

# ---------------------------------------------------------------
# Read input file and extract images
# ---------------------------------------------------------------


def read_input(inputFile: str, verbose: bool = False):
    '''
    Read input file and extract images
    input:
        inputFile: input PDF file (str)
        verbose: additional prints for debugging (bool)
    output:
        images: list of images (list)
    '''
    if verbose:
        print(
            f"{bcolors.OKBLUE}Reading {inputFile} and converting each page to image...{bcolors.ENDC}")
    createDir('/tmp/test-api/images', True)

    # check if input file exists and is proper format
    if check_file(inputFile):
        # read file and convert it to images
        readPDF(inputFile)
