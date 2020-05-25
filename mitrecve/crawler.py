"""
Get the vulnerabilities from different source (See docs/vuln-source.md) for each package found
"""
import json
import requests
from bs4 import BeautifulSoup
MAX_WORKER = 15

############################
##### CVE MITRE Source #####
############################
# https://cve.mitre.org/cve/search_cve_list.html

# No API but you can download the source in differents format XML, CSV ... but these are heavy file 
# It's more pratical to make little requests
# So let's go make a litle API with beautifulsoup and requests

# Add souptrainer and lxml

import lxml.html as lh
from pprint import pprint

def MITRE_get_main_page(package): 
    """
    Get all the CVE for a package/keyword
    """
    base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=" + package # package can be a keyword or a CVE ID or a list of Keyword/CVE ID (separate with a +) 
    cve_group = []
    

    document = lh.fromstring(requests.get(base_url).text)

    cve_entries = document.cssselect("div#TableWithRules table tr > td") # List of <tr> entries for CVE in main page

    for i in range(0, len(cve_entries) , 2):
        cve_group.append(
            (
                cve_entries[i].text_content(),
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_entries[i].text_content(),
                cve_entries[i+1].text_content()
            )
        )
    return cve_group 


# Getter
def get_cve_links(package) :
    cve_links = []
    cve_group = MITRE_get_main_page(package)
    for cve in cve_group :
        cve_links.append(cve[1])
    return cve_links

def get_cve_id(package) :
    cve_id = []
    cve_group = MITRE_get_main_page(package)
    for cve in cve_group :
        cve_id.append(cve[0])

def get_cve_desc(package) :
    cve_desc = []
    cve_group = MITRE_get_main_page(package)
    for cve in cve_group :
        cve_desc.append(cve[1])
    return cve_desc

def MITRE_get_cve_detail(package):
    cve_group = MITRE_get_main_page(package)
    cve_detail = []
    cve_ref = []
    nvd_links = []


    def get_links():
        listLinks = []
        for i in range(len(cve_group)) :
            listLinks.append(cve_group[i][1])
        return listLinks
    
    links = get_links()

    # Big loop -> need opti
    for l in links: 
        rq = requests.get(l).text
        soup = BeautifulSoup(rq, 'html.parser')
        
        ## reference links
        ref_links = soup.select("#GeneratedTable > table > tr > td > ul")[0].find_all("a") 
        ## Get NVD links for more detail
        more = soup.select("#GeneratedTable .ltgreybackground .larger")[0].find("a")["href"]

        # save nvd links else you will have only the first one in the cve_detail list (for each cve)
        nvd_links.append(more)

        # DEBUG print(l, more, type(more))
        # construct list of reference links 
        for ref in ref_links : 
            cve_ref.append(ref["href"])

        # Clean cve_ref for the next cve_reference links 
        # else you add all links in all cve
        tmp_ref = cve_ref
        cve_ref = []

    # construct final list 
    # data struct : 
    # [(cve_name, cve_desc, more_cve_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (cve_name, cve_desc, more_cve_n, [ref_1_cve_n, ref_2_cve_n])]
    for i in range(len(cve_group)) :
        cve_detail.append(
            (
                cve_group[i][0],
                cve_group[i][-1],
                nvd_links[i],
                tmp_ref
                # add more data here
            )
        )

    return cve_detail 

###########################
###### CVE MITRE API ######
###########################

# get data for a CVE-ID 
def download(url):
    document = lh.fromstring(requests.get(url, stream=True).text)  
    cve_ref = []     #  reference links
    
    cve_detail = []  #  [(cve_name, cve_desc, more_cve_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (cve_name, cve_desc, more_cve_n, [ref_1_cve_n, ref_2_cve_n])]

    # SELECTOR
    ## Ref Selector
    ref_selector = document.cssselect("div#GeneratedTable table tr td ul li a")

    for c in ref_selector:
        cve_ref.append(c.get("href"))
    # DEBUG   pprint(cve_ref)

    ## NVD Selector
    nvd_selector = document.cssselect("div#GeneratedTable .ltgreybackground a")
    nvd_links = nvd_selector[0].get("href")
    # DEBUGpprint(nvd_links)

    ## Assinging CNA Selector
    cna_selector = document.cssselect("div#GeneratedTable table tr:nth-child(9)")
    cna = cna_selector[0].text_content().strip()
    # DEBUGpprint(cna)

    ## Date entry Selector
    date_selector = document.cssselect("div#GeneratedTable table tr:nth-child(11) td b")
    date = date_selector[0].text_content()
    date = date[0:4] + "/" + date[4:6] + "/" + date[6:]
    # DEBUG pprint(date)


    # Output a couple composed of (cve_name, cve_desc, nvdlinks, [cve_ref])
    return (cve_ref, nvd_links, cna, date)


def MITRE_get_cve_detail_opti(package):  

    links = get_cve_links(package)


    from concurrent.futures import ThreadPoolExecutor, as_completed
    from time import time
    # multithreading
    start = time()
    processes = []

    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        for url in links:
            processes.append(executor.submit(download, url))

    for task in as_completed(processes):
        pprint(task.result())

    print(f'Time taken: {time() - start}')

## OPTI STEP :
# Get all CVE url from main page 
# Construct url pool with multi threading 
# Make request   


## SAME IMPLEMENTATION
# Search by CVE-ID
# @require : exact CVE ID 

# Search by Keyword : 

# search by multiple keywords

