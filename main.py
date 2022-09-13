#from imageai.Detection import ObjectDetection
#from lib.FirstDetection import first_detection_image

from lib.utils import *
from lib.readData import *

# ---------------------------------------------------------------
# ma6in
# ---------------------------------------------------------------
def main():  

    # parse options from command line
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: %prog arguments", version="%prog")
    parser.add_option("-r",  "--read",       dest="read",     action='store_true',   help="Read files and extract images (default: %default)")
    parser.add_option("-c",  "--config",     dest="config",                          help="Name of your configuration file(default: %default)")
    parser.add_option("-v",  "--verbose",    dest="verbose",  action='store_true',   help="Additional prints for debugging (default: %default)")
    parser.set_defaults(read=False, config='config/config.ini', verbose=False)
    (options,args) = parser.parse_args()

    if options.verbose:
        print(f"{bcolors.OKBLUE}Verbose mode enabled!{bcolors.ENDC}")

    # Read configuration file
    params = readConfig(options.config, options.verbose)

    # Read all files and extract images in png format
    if options.read:
        images = read_data(params)

    print ("hello")
    #first_detection_image()

    


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == '__main__':
    main()