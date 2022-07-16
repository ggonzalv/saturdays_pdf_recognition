import os,sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ---------------------------------------------------------------
# Create Directory if NOT exists
# ---------------------------------------------------------------
def createDir(directory: str):
    '''
    Create directory if not exists
    
    input:
        directory: name of directory (str)
    '''
    if not os.path.exists(directory):
        try: 
            os.makedirs(directory)
        except OSError:
            if os.path.islink(directory):
                os.remove(directory)
                os.makedirs(directory)
            else:
                print(f"{bcolors.FAIL}Error: Directory {directory} cannot be created!{bcolors.ENDC}")
                sys.exit()

# ---------------------------------------------------------------
# Read Configuration File
# ---------------------------------------------------------------
def readConfig(configFile, verbose=False):
    '''
    Read configuration file parameters

    input:
        configFile: name of the configuration file (str)
        verbose: additional prints for debugging (bool)
    output:
        parameters: dictionary of read parameters (dict)
    '''
    parameters = {}

    try:
        with open(configFile, 'r') as InputFile:
            while 1:
                line = InputFile.readline()
                if not line: break
                if '#' not in line and len(line) > 1 :
                    command = line.split("=")
                    parameters[command[0].strip()] = eval(command[1].strip())

        if verbose:
            print(f"{bcolors.OKBLUE}Configuration parameters: {parameters}{bcolors.ENDC}")
        return parameters
    except IOError:
        print(f"File {configFile} does not exist!")
        sys.exit()