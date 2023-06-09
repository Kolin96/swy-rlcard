class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED =  '\033[91m'
    CYAN = '\033[96m'
    
def color_your_oppo(you_oppo):
    return bcolor.RED + you_oppo + bcolor.ENDC

def color_you(you):
    return bcolor.CYAN + you + bcolor.ENDC

def bold(input):
    if type(input) == str:
        return bcolor.BOLD + input + bcolor.ENDC
    elif type(input) == list:
        return [bcolor.BOLD + bcolor.UNDERLINE + i + bcolor.ENDC for i in input]