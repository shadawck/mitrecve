"""
Get the CVE from Mitre based on requested packages/keyword/CVE-ID
"""
import lxml.html as lh
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
MAX_WORKER = 15

# https://cve.mitre.org/cve/search_cve_list.html

# There is no API for Mitre CVE but you can download the source in differents format XML, CSV ... but these are heavy file
# It's more pratical to make little requests
# So let's go make a litle API with lxml and requests

###########################
###### CVE MITRE API ######
###########################



def get_main_page(package): 
    """Main function to get cve

    Get all the CVE for a package/keyword. These are valid string:

    * Make multiple package request at the same time : ``get_main_page("package1,package2")``
    * Use several keyword to narrow a research : ``get_main_page("keyword1+keyword2"``
    * And a combination of the above options : ``get_main_page("keyword1+keyword2,package1,package2")``. Here there will be 3 differents requests.

    Args:
        package (str): package, keyword you want to search for

    Return:
        List: List of Tuple composed of all the CVE found for the choosen package. 
        
        Data Structure: [(cve_id_0, cve_link_0, cve_desc_0) ,..., (cve_id_n, cve_link_n, cve_desc_n)]

    Examples:
    
    * Example for a simple package request::

        >> crawler.get_main_page("jython")
        
        [
            ('CVE-2016-4000',
                'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4000',
                'Jython before 2.7.1rc1 allows attackers to execute arbitrary code via a '
                'crafted serialized PyFunction object.'
            ),
         
            ('CVE-2013-2027',
                'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-2027',
                'Jython 2.2.1 uses the current umask to set the privileges of the class '
                'cache files, which allows local users to bypass intended access '
                'restrictions via unspecified vectors.'
            )
        ]

    """

    base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=" + package # package can be a keyword or a CVE ID or a list of Keyword/CVE ID (separate with a +) 
    cve_group = []
    

    document = lh.fromstring(requests.get(base_url).text)

    cve_entries = document.cssselect("div#TableWithRules table tr > td") # List of <tr> entries for CVE in main page

    for i in range(0, len(cve_entries) , 2):
        cve_group.append(
            (
                cve_entries[i].text_content(), # CVE ID 
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_entries[i].text_content(), # CVE link
                cve_entries[i+1].text_content() # CVE description
            )
        )
    return cve_group 


# Getter from main page
## Pointless for now
def get_cve_links(package) :
    cve_links = []
    cve_group = get_main_page(package)
    for cve in cve_group :
        cve_links.append(cve[1])
    return cve_links

def get_cve_id(package) :
    cve_id = []
    cve_group = get_main_page(package)
    for cve in cve_group :
        cve_id.append(cve[0])

def get_cve_desc(package) :
    cve_desc = []
    cve_group = get_main_page(package)
    for cve in cve_group :
        cve_desc.append(cve[1])
    return cve_desc

def get_cve_detail(package):
    """Main function to get cve **details**

    Get all the CVE for a package/keyword with details. These are valid string:

    * Make multiple package request at the same time : ``get_cve_detail("package1,package2")``
    * Use several keyword to narrow a research : ``get_cve_detail("keyword1+keyword2"``
    * And a combination of the above options : ``get_cve_detail("keyword1+keyword2,package1,package2")``. Here there will be 3 differents requests.

    Args:
        package (str): package, keyword you want to search for

    Return:
        List: List of Tuple composed of all the CVE found for the choosen package. 
        
        Data Structure: [(cve_name, cve_desc, nvd_link_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (cve_name, cve_desc, nvd_link_n, [ref_1_cve_n, ref_2_cve_n])]

    Examples:

    * Example for a simple package request::

        >> crawler.get_cve_detail("jython")
        [
            ('CVE-2016-4000',
                'Jython before 2.7.1rc1 allows attackers to execute arbitrary code via a '
                'crafted serialized PyFunction object.', # cve description
                'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-4000',
                ['http://advisories.mageia.org/MGASA-2015-0096.html',
                 'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
                 'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
                 'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
                 'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html']
            ),
         
            ('CVE-2013-2027',
                'Jython 2.2.1 uses the current umask to set the privileges of the class '
                'cache files, which allows local users to bypass intended access '
                'restrictions via unspecified vectors.',
                'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-2027',
                ['http://advisories.mageia.org/MGASA-2015-0096.html',
                 'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
                 'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
                 'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
                 'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html']
            )
        ]

    """
    cve_group = get_main_page(package)
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
                # add more data here (future version)
            )
        )

    return cve_detail 


##### WORKING ON OPIMISATION
# Not for the current version

def get_main():
    # Create a function like get_detail with lxml and coonstructed for multiprocessing (like get_cve_detail_opti )
    pass

def get_detail(url):
    # Add name, description and more like the non-optimized one


    document = lh.fromstring(requests.get(url, stream=True).text)  
    cve_ref = []     #  reference links
    
    cve_detail = []  #  [(cve_name, cve_desc, more_cve_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (cve_name, cve_desc, more_cve_n, [ref_1_cve_n, ref_2_cve_n])]

    # SELECTOR
    ## Reference Selector -> reference link and source
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

def get_cve_detail_opti(package):  

    links = get_cve_links(package)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from time import time
    # multithreading
    start = time()
    processes = []

    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        for url in links:
            processes.append(executor.submit(get_detail, url))

    #for task in as_completed(processes):
    #    pprint(task.result()[0])

    return [task.result() for task in as_completed(processes)]

    print(f'Time taken: {time() - start}')

## OPTI STEP :
# Get all CVE url from main page 
# Construct url pool with multi threading 
# Make request