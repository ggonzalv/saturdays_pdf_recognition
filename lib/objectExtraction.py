import cv2
from lib.utils import *
from lib.tableHandler import *

# ---------------------------------------------------------------
# Extract tables and images from PDF files
# ---------------------------------------------------------------
def extractResults(tables, extension, figures, image, page: int):
    '''
    Extract tables and images from PDF files
    
    input:
        tables: list of tables 
        extension: extension for output tables (str)
        figures: list of figures 
        image: input image
        page: page number (int)
    '''
    if tables:
        for index, tab in enumerate(tables):
            coords= getPixelCoordinates(tab)
            suffix = f'_pg{page}_tab{index}'
            extractTable(coords, extension, image, suffix)
    if figures:
        for index, fig in enumerate(figures):
            coords = getPixelCoordinates(fig)
            suffix = f'_pg{page}_fig{index}'
            extractFigure(coords, image, suffix)

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
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # By default OpenCV reads images in BGR format
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
    cv2.imwrite(f'output/figure{suffix}.jpg', img)

# ---------------------------------------------------------------
# Get coordinates from torch tensor
# ---------------------------------------------------------------
def getPixelCoordinates(box):
    '''
    Get coordinates from torch tensor
    
    input:
        box: torch tensor
    '''
    return list(map(round,box.tolist()))