#from imageai.Detection import ObjectDetection
from lib.imageModel import *
from lib.utils import *
from lib.readData import *

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
    parser.add_option("-v",  "--verbose",    dest="verbose",  action='store_true',   help="Additional prints for debugging (default: %default)")
    parser.set_defaults(read=False, config='config/config.ini', input='', verbose=False)
    (options,args) = parser.parse_args()

    if options.verbose:
        print(f"{bcolors.OKBLUE}Verbose mode enabled!{bcolors.ENDC}")

    # Read configuration file
    params = readConfig(options.config, options.verbose)

    # Read all files and extract images in png format
    if options.read:
        images = read_data(params)

    # Load model and image to predict
    model = loadPredictor(params)
    image = loadImage(options.input)

    # Extract tables and figures boxes
    boxes = predictImage(model, image)

    # Visualize results
    visualizePredictions(boxes, image, params['outputFile'])

    

    


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == '__main__':
    main()