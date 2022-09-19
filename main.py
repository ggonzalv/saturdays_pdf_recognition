#from imageai.Detection import ObjectDetection
from lib.imageModel import *
from lib.utils import *
from lib.readData import *
from lib.objectExtraction import *

# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------


def main():

    # parse options from command line
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog arguments", version="%prog")
    parser.add_option("-r",  "--read",       dest="read",     action='store_true',
                      help="Read files and extract images (default: %default)")
    parser.add_option("-c",  "--config",     dest="config",
                      help="Name of your configuration file (default: %default)")
    parser.add_option("-i",  "--input",     dest="input",
                      help="Input file to extract tables and figures (default: %default)")
    parser.add_option("-e",  "--extension",     dest="extension",
                      help="Extension to extract tables (docx, xlsx, tex) (default: %default)")
    parser.add_option("-t",  "--table",     dest="table",
                      help="Path to table in jpg/png format to turn into editable file (default: %default)")
    parser.add_option("-v",  "--verbose",    dest="verbose",  action='store_true',
                      help="Additional prints for debugging (default: %default)")
    parser.set_defaults(read=False, config='config/config.ini',
                        input='', extension="docx", table='', verbose=False)
    (options, args) = parser.parse_args()

    verbose = options.verbose
    if verbose:
        print(f"{bcolors.OKBLUE}Verbose mode enabled!{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}Configuration file: {options.config}")

    if options.extension not in ["docx", "xlsx", "tex"]:
        print(f"{bcolors.FAIL}Unknown extension {options.extension} for table conversion. Please select between (docx, xlsx, tex){bcolors.ENDC}")
        sys.exit()
    # Read configuration file
    params = readConfig(options.config, verbose)

    createDir('tmp_output_files', True)
    createDir('output_visualization')
    if verbose:
        print(f"{bcolors.OKBLUE}Output directories {bcolors.ENDC}{bcolors.OKGREEN}tmp_output_files{bcolors.ENDC}{bcolors.OKBLUE} and {bcolors.ENDC}{bcolors.OKGREEN}output_visualization{bcolors.ENDC}{bcolors.OKBLUE} successfully created{bcolors.ENDC}")

    # Read all files and extract images in png format
    if options.read:
        if verbose:
            print(f"{bcolors.OKBLUE}Entering training mode{bcolors.ENDC}")
        trainImages = read_data(params)

    if options.table:

        if verbose:
            print(f"{bcolors.OKBLUE}Entering table mode{bcolors.ENDC}")
            print(f"{bcolors.OKBLUE}Converting table {options.table}{bcolors.ENDC}")

        image = loadImage(options.table)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        tableConvertor(image, options.extension,
                       options.table.replace(".jpg", "").replace(".png", ""), True)
        print(f"{bcolors.OKGREEN}Table {options.table} converted to {options.extension} format in and stored in {options.table.replace('.jpg', '').replace('.png', '')}.{options.extension}{bcolors.ENDC}")
        sys.exit()

    # Load model
    model = loadPredictor(params, verbose)
    print(f"{bcolors.OKGREEN}Model successfully loaded!{bcolors.ENDC}")

    # Load pdf images and convert to cv2 format
    read_input(options.input, verbose)
    images = [loadImage(f'tmp/{image}') for image in sorted(os.listdir('tmp'))]
    print(f"{bcolors.OKGREEN}Input file successfully read!{bcolors.ENDC}")

    # Extract tables and figures boxes
    print(f"{bcolors.OKGREEN}Applying model to each page and extracting tables and figures")
    for i, image in enumerate(images):
        if verbose:
            print(f"{bcolors.OKBLUE}Reading page {i+1}...{bcolors.ENDC}")
        boxes = predictImage(model, image)
        tables = boxes[(boxes.pred_classes == 3) & (
            boxes.scores > 0.7)].pred_boxes  # 3 is table class
        figures = boxes[(boxes.pred_classes == 4) & (
            boxes.scores > 0.7)].pred_boxes  # 4 is figure class
        extractResults(tables, options.extension, figures, image, i, verbose)
        # Visualize results
        visualizePredictions(
            boxes, image, f"output_visualization/{params['outputFile']}_pg{i+1}.png", verbose)
    compressOutput(verbose)
    print(f"{bcolors.OKGREEN}Output successfully stored in {bcolors.ENDC}{bcolors.OKBLUE}output.zip{bcolors.ENDC}")
    cleanDirectories()


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == '__main__':
    main()
