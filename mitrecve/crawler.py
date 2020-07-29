"""
Get the CVE from Mitre based on requested packages/keyword/CVE-ID
"""
import lxml.html as lh
import json
import requests
import multiprocessing
from functools import partial
from pprint import pprint


MAX_WORKER = 15

# https://cve.mitre.org/cve/search_cve_list.html

# There is no API for Mitre CVE but you can download the source in differents format XML, CSV ... but these are heavy file
# It's more pratical to make little requests
# So let's go make a litle API with lxml and requests

###########################
###### CVE MITRE API ######
###########################


def get_main_page(__format,package): 
    """Main function to get cve

    Get all the CVE for a package/keyword. These are valid string:

    * Make multiple package request at the same time : ``get_main_page("package1,package2")``
    * Use several keyword to narrow a research : ``get_main_page("keyword1+keyword2")``
    * And a combination of the above options : ``get_main_page("keyword1+keyword2,package1,package2")``. Here there will be 3 differents requests.

    Args:
        package (str): package, keyword you want to search for

    Return:
        dict. A dict with an entry for each CVE with these keyword : ID,URL,DESC

    Examples:
    
    * Example for a simple package request::

        >> crawler.get_main_page("jython")
        
        {
            0: {
                'DESC': 'Jython before 2.7.1rc1 allows attackers to execute arbitrarycode via a crafted serialized PyFunction object.',
                'ID': 'CVE-2016-4000',
                'URL': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4000'
            },
            
            1: {
                'DESC': 'Jython 2.2.1 uses the current umask to set the privileges of the class cache files, which allows local users to bypass intended access restrictions via unspecified vectors.',
                'ID': 'CVE-2013-2027',
                'URL': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-2027'
            }
        }

    """
    dictMain = {}
    id = 0 
    
    base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=" + package # package can be a keyword or a CVE ID or a list of Keyword/CVE ID (separate with a +) 
    cve_group = []
    document = lh.fromstring(requests.get(base_url).text) 
    cve_entries = document.cssselect("div#TableWithRules table tr > td") # List of <tr> entries for CVE in main page

    # Write package cve data in dictionnary
    for i in range(0, len(cve_entries) , 2):
        dictMain[id] = {
            "ID"   : cve_entries[i].text_content(),
            "URL"  : "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_entries[i].text_content(),
            "DESC" : cve_entries[i+1].text_content().strip()
        }
        id +=1


    if __format=="json":
        with open("./output/"+ package + ".json", 'w') as fp:
            json.dump(dictMain, fp)

    return dictMain

def main_cves(__format,package):
    func = partial(get_main_page,__format)

    with multiprocessing.Pool() as p:
        dictList = p.map(func, package)
    
    return dictList

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
    processes = []

    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        for url in links:
            processes.append(executor.submit(get_detail, url))

    return [task.result() for task in as_completed(processes)]
