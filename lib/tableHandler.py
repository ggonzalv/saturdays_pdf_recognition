import pytesseract
from pytesseract import Output
import docx
import pandas as pd

from lib.utils import clean_df, get_columns, bcolors

# ---------------------------------------------------------------
# Convert image table to specific format
# ---------------------------------------------------------------
def tableConvertor(img, ext: str, suffix: str):
    # sourcery skip: move-assign, switch
    '''
    Convert string data table to specific format and save
    input:
        image: image to extract text from
        ext: extension for output tables (str)
        suffix: suffix for output file
    '''
    myconfig = r"-c preserve_interword_spaces=1 --oem 3 --psm 6"
    data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT, lang='eng')  
    df = pd.DataFrame(data)
    # Clean dataframe
    df = clean_df(df)
    # Extract columns 
    df = get_columns(df)
    # Group by lines
    cells = df.groupby(['line_num']).apply(list).tolist()
    nrows, ncols = len(cells), len(cells[0])
    # Convert to specific format
    if ext == "tex":
        makeLatex(cells, ncols, suffix)
    elif ext == "docx":
        createWord(cells, nrows, ncols, suffix)
    elif ext == "xls":
        createExcel(cells,suffix)
    else:
        print(f"{bcolors.FAIL}Unknown extension {ext}{bcolors.ENDC}")
        return None



# ---------------------------------------------------------------
# Make latex table
# ---------------------------------------------------------------
def makeLatex(rows: list, ncols: int, suffix: str):
    '''
    Make latex table
    input:
        rows: list of rows with text (list)
        ncols: number of columns (int)
        suffix: suffix of the table (str)
    '''
    header = makeHeader(ncols)
    body = makeBody(rows)
    footer = makeFooter()

    with open(f"output/table{suffix}.tex", "w+") as f:
        f.write(header+body+footer)

# ---------------------------------------------------------------
# Make latex header
# ---------------------------------------------------------------
def makeHeader(ncols: int):
    '''
    Make latex header
    input:
        ncols: number of columns (int)
    '''
    header  = "\\begin{table}[!ht]\n"
    header += "\\begin{center}\n"
    header += "\\begin{tabular}{%s}\n"%("l"+"c"*(ncols-1))
    header += "\hline\hline \n"
    return header

# ---------------------------------------------------------------
# Make latex body
# ---------------------------------------------------------------
def makeBody(rows: list):
    '''
    Make latex body
    input:
        rows: list of rows with text (list)
    '''
    body = ""
    for row in rows:
        if not row: continue
        row =  " & ".join(row).replace("_", "\\_")
        body += row+"\\\\\n"
    return body

# ---------------------------------------------------------------
# Make latex footer
# ---------------------------------------------------------------
def makeFooter():
    '''
    Make latex footer
    '''
    footer  = "\n\hline\n\hline\n\end{tabular}\n"
    #footer += "\caption{}\n" 
    footer += "\end{center}\n\end{table}"
    return footer

# ---------------------------------------------------------------
# Make Word table
# ---------------------------------------------------------------
def createWord(rows: list, nrows: int, ncols: int, suffix: str):
    '''
    Make word table
    input:
        rows: list of rows with text (list)
        nrows: number of rows (int)
        ncols: number of columns (int)
    '''
    doc = docx.Document()
    table = doc.add_table(rows=nrows, cols=ncols)
    for i, row in enumerate(rows):
        if not row: continue
        wordRow = table.rows[i].cells
        for j, item in enumerate(row):
            wordRow[j].text = item
    
    doc.save(f"output/table{suffix}.docx")

# ---------------------------------------------------------------
# Make Excel table
# ---------------------------------------------------------------
def createExcel(cells: list, suffix: str):
    '''
    Make excel table
    input:
        cells: cells of dataframe (list)
        suffix: suffix of the table (str)
    '''
    header = cells.pop(0)
    df = pd.DataFrame(cells)
    try:
        df.to_excel(f"output/table{suffix}.xlsx", header=header)
    except ValueError:
        print(f"{bcolors.WARNING}Something went wrong when reading table{suffix}. Please check out the output file{bcolors.ENDC}")
        df.to_excel(f"output/table{suffix}.xlsx")
    return df