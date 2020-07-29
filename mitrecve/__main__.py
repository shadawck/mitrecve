#!/usr/bin/env python3
# __main__.py

"""MitreCVE

Basic usage:
  mitrecve crawl <package> [--verbose --detail ] [--format FORMAT]
  mitrecve show <result>
  mitrecve ( -h | --help | --version )

options:
    -f --format FORMAT  Choose output format
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
from glom import glom
import subprocess
import os

def main():
    """
    Implement CLI logic 
    """
    arguments = docopt(__doc__, version='mitrecve 1.0.5')
    #print(arguments)
    
    ############## CLI VAR ################
    __crawl      = arguments["crawl"]
    __show       = arguments["show"]

    ##### CRAWLING COMMAND ######
    if __crawl:
        __verbose    = arguments["--verbose"]
        __detail     = arguments["--detail"]
        __package    = arguments["<package>"].split(',') 
        __format     = arguments["--format"]

        if __detail:
            utility.print_vulnerabilites_detail(__package,__verbose)
        else : 
            #utility.print_vulnerabilites(__package,__verbose)
            crawler.main_cves(__format,__package)
    
    ####### SHOW COMMAND #########
    elif __show:
        __result  = arguments["<result>"] + ".json"
        files = os.listdir("./output/")
        if __result in files:
            subprocess.run(["jq", ".","output/"+__result])  # doesn't capture output
        else :
            print("Crawl first then look at the result not the inverse !!!\n")


    

if __name__ == "__main__":
    main()
