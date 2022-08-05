import cv2
from lib.utils import *

# ---------------------------------------------------------------
# Extract tables and images from PDF files
# ---------------------------------------------------------------
def extractResults(tables, figures, image, page: int):
    '''
    Extract tables and images from PDF files
    
    input:
        tables: list of tables 
        figures: list of figures 
        image: input image
        page: page number (int)
    '''
    if tables:
        for index, tab in enumerate(tables):
            coords= getPixelCoordinates(tab)
            suffix = f'_pg{page}_tab{index}'
            extractTable(coords, image, suffix)
    if figures:
        for index, fig in enumerate(figures):
            coords = getPixelCoordinates(fig)
            suffix = f'_pg{page}_fig{index}'
            extractFigure(coords, image, suffix)

# ---------------------------------------------------------------
# Extract table from PDF file
# ---------------------------------------------------------------
def extractTable(table, image, suffix: str):
    '''
    Extract table from PDF file
    
    input:
        table: table (np.array)
        image: input image
        suffix: suffix for output file
    '''
    img = image[table[1]:table[3], table[0]:table[2]]
    cv2.imwrite(f'output/table{suffix}.jpg', img)

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