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
    parser = OptionParser(usage = "usage: %prog arguments", version="%prog")
    parser.add_option("-r",  "--read",       dest="read",     action='store_true',   help="Read files and extract images (default: %default)")
    parser.add_option("-c",  "--config",     dest="config",                          help="Name of your configuration file (default: %default)")
    parser.add_option("-i",  "--input",     dest="input",                          help="Input file to extract tables and figures (default: %default)")
    parser.add_option("-e",  "--extension",     dest="extension",                          help="Extension to extract tables (docx, xls, tex) (default: %default)")
    parser.add_option("-t",  "--table",     dest="table",                          help="Path to table in jpg format to turn into editable file (default: %default)")
    parser.add_option("-v",  "--verbose",    dest="verbose",  action='store_true',   help="Additional prints for debugging (default: %default)")
    parser.set_defaults(read=False, config='config/config.ini', input='', extension="docx", table='', verbose=False)
    (options,args) = parser.parse_args()

    if options.verbose:
        print(f"{bcolors.OKBLUE}Verbose mode enabled!{bcolors.ENDC}")

    # Read configuration file
    params = readConfig(options.config, options.verbose)

    # Read all files and extract images in png format
    if options.read:
        trainImages = read_data(params)
        
    if options.table:
        image = loadImage(options.table)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        tableConvertor(image, options.extension, f'_{options.table.replace(".jpg", "")}')
        sys.exit("Table converted and stored in output folder")

    # Load model 
    model = loadPredictor(params)

    # Load pdf images and convert to cv2 format
    read_input(options.input, options.verbose)
    images = [loadImage(f'tmp/{image}') for image in sorted(os.listdir('tmp'))]

    # Extract tables and figures boxes
    createDir('output', True)
    for i, image in enumerate(images):
        boxes = predictImage(model, image)
        tables = boxes[(boxes.pred_classes == 3) & (boxes.scores > 0.7)].pred_boxes # 3 is table class
        figures = boxes[(boxes.pred_classes == 4) & (boxes.scores > 0.7)].pred_boxes # 4 is figure class
        extractResults(tables, options.extension, figures, image, i)
        # Visualize results
        createDir('output_visualization')
        visualizePredictions(boxes, image, f"output_visualization/{params['outputFile']}_pg{i+1}.png")

    

    


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == '__main__':
    main()