from utils import *

# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------
def main():  

    # parse options from command line
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog arguments", version="%prog")
    parser.add_option("-n","--fileName",        dest="fileName",                          help="Name of your input file, for tests only (default: %default)")
    parser.add_option("-p","--npages",        dest="npages",       type=int,                   help="Specify number of pages to read, for tests only (default: %default)")
    parser.add_option("-i","--inputDir",        dest="inputDir",                       help="Input directory with files to read (default: %default)")
    parser.add_option("-f","--nFiles",        dest="nFiles",    type=int,                   help="Number of files to read (default: %default)")
    parser.set_defaults(fileName="", npages=-1, inputDir="data", nFiles=-1)
    (options,args) = parser.parse_args()

    tFile = options.fileName
    npages = options.npages
    inputDir = options.inputDir
    nFiles = options.nFiles

    # Create output directory if not exist
    createDir("images")

    # For tests only. Read just one file
    if tFile:
        # check if input file exists and is proper format
        if check_file(tFile):
            print(f"{bcolors.OKGREEN}Reading {tFile} and extracting images...{bcolors.ENDC}")
            # read file and convert it to images
            images = readPDF(tFile, npages)

    elif inputDir:
        # Read all files in directory
        images = read_files(inputDir, nFiles)


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == '__main__':
    main()