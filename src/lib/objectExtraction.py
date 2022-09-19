import cv2
from lib.utils import *
from lib.tableHandler import *

# ---------------------------------------------------------------
# Extract tables and images from PDF files
# ---------------------------------------------------------------


def extractResults(tables, extension, figures, image, page: int, verbose: bool = False):
    '''
    Extract tables and images from PDF files

    input:
        tables: list of tables 
        extension: extension for output tables (str)
        figures: list of figures 
        image: input image
        page: page number (int)
        verbose: additional prints for debugging
    '''
    if tables:
        if verbose:
            print(f"{bcolors.OKBLUE}Extracting tables...{bcolors.ENDC}")
        for index, tab in enumerate(tables):
            coords = getPixelCoordinates(tab)
            suffix = f'_pg{page}_tab{index}'
            extractTable(coords, extension, image, suffix)
    if figures:
        if verbose:
            print(f"{bcolors.OKBLUE}Extracting figures...{bcolors.ENDC}")
        for index, fig in enumerate(figures):
            coords = getPixelCoordinates(fig)
            suffix = f'_pg{page}_fig{index}'
            extractFigure(coords, image, suffix)
    if verbose:
        print(
            f"{bcolors.OKBLUE}Successfully extracted tables and figures!{bcolors.ENDC}")


# ---------------------------------------------------------------
# Extract table from PDF file
# ---------------------------------------------------------------


def extractTable(table, extension, image, suffix: str):
    '''
    Extract table from PDF file

    input:
        table: table (np.array)
        extension: extension for output tables (str)
        image: input image
        suffix: suffix for output file
    '''
    img = image[table[1]:table[3], table[0]:table[2]]
    # By default OpenCV reads images in BGR format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tableConvertor(img, extension, suffix)


# ---------------------------------------------------------------
# Extract table from PDF file
# ---------------------------------------------------------------
def extractFigure(figure, image, suffix: str):
    '''
    Extract figure from PDF file

    input:
        fig: fig (np.array)
        image: input image
        suffix: suffix for output file
    '''
    img = image[figure[1]:figure[3], figure[0]:figure[2]]
    cv2.imwrite(f'/tmp/test-api/tmp_output_files/figure{suffix}.jpg', img)

# ---------------------------------------------------------------
# Get coordinates from torch tensor
# ---------------------------------------------------------------


def getPixelCoordinates(box):
    '''
    Get coordinates from torch tensor

    input:
        box: torch tensor
    '''
    return list(map(round, box.tolist()))
