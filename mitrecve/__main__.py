#!/usr/bin/env python3
# __main__.py

"""MitreCVE

Basic usage:
  mitrecve <package> [--verbose --detail ] [-o FILE - FORMAT] 
  mitrecve ( -h | --help | --version )

options:
    -f  --format FORMAT  Choose output format
    -o --output FILE     Save output to file
    -v --verbose         Show full output
    -d --detail          Show CVE details
    -h --help            Show this screen
       --version         Show version

"""

import sys
from docopt import docopt
from mitrecve import utility
from mitrecve import crawler
from pprint import pprint

def main():
    """
    Implement CLI logic 
    """
    arguments = docopt(__doc__, version='mitrecve 1.0.0')
    
    ############## CLI VAR ################
    __verbose    = arguments["--verbose"]
    __detail     = arguments["--detail"]
    __package    = arguments["<package>"].split(',') 
    __output     = arguments["--output"]
    __format     = arguments["--format"]
    if __output   :  __output_ext = __output.split(".")[0]
    
    ############# OUPUT STDOUT ############

    ### CVE print
    if __detail:
        utility.print_vulnerabilites_detail(__package,__verbose)
    else : 
        #utility.print_vulnerabilites(__package,__verbose)
        crawler.get_main_page(__package,__verbose)

if __name__ == "__main__":
    main()
