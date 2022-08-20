#!/usr/bin/env python3
# __main__.py

"""MitreCVE

Basic usage:
  mitrecve crawl <package> [--detail ] [--format FORMAT]
  mitrecve show <result>
  mitrecve ( -h | --help | --version )

options:
    -f --format FORMAT   Choose output format (json)
    -d --detail          Show CVE details
    -h --help            Show this screen
       --version         Show version
"""

from docopt import docopt
from mitrecve import utility
from mitrecve import crawler
import subprocess
import os
import json

def main():
    """
    Implement CLI logic 
    """
    arguments = docopt(__doc__, version='mitrecve 1.1.1')

    ############## CLI VAR ################
    __crawl      = arguments["crawl"]
    __show       = arguments["show"]

    ##### CRAWLING COMMAND ######
    if __crawl:
        __detail     = arguments["--detail"]
        __package    = arguments["<package>"].split(',')
        __format     = arguments["--format"]

        for pack in __package:
            print("\n-------------- Package: <" + pack + "> --------------")

            cve = crawler.get_main_page(pack)
            if __detail:
                cve = crawler.get_cve_detail(cve)
                utility.print_vulnerabilites_detail(cve)
            else : 
                utility.print_vulnerabilites(cve)
            
            if __format == 'json' :
                path = "./output"
                exist = os.path.exists(path)
                if not exist:
                    os.makedirs(path)
                
                with open("./output/"+ pack + ".json", 'w') as fp:
                    json.dump(cve, fp)

    
    ####### SHOW COMMAND #########
    elif __show:
        __result  = arguments["<result>"] + ".json"
        if os.path.exists("./output/"):
            files = os.listdir("./output/")

            if __result in files:
                subprocess.run(["jq", ".","output/"+__result])
                print("print")
            else :         
                print("Crawl first then look at the result !!!")
                print("Try : \n\tmitrecve crawl", __result, "-f json" )
        else :
            print("Crawl first then look at the result !!!")
            print("Try : \n\tmitrecve crawl", __result, "-f json" )


if __name__ == "__main__":
    main()
