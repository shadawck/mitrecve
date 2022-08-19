"""
Get the CVE from Mitre based on requested packages/keyword/CVE-ID
"""

import lxml.html as lh
import requests

# https://cve.mitre.org/cve/search_cve_list.html

# There is no API for Mitre CVE but you can download the source in differents format XML, CSV ... but these are heavy file
# It's more pratical to make little requests
# So let's go make a litle API with lxml and requests

###########################
###### CVE MITRE API ######
###########################


def get_main_page(__package): 
    """Main function to get cve

    Get all the CVE for a __package/keyword. These are valid string:

    * Make multiple __package request at the same time : ``get_main_page("package1,package2")``
    * Use several keyword to narrow a research : ``get_main_page("keyword1+keyword2")``
    * And a combination of the above options : ``get_main_page("keyword1+keyword2,package1,package2")``. Here there will be 3 differents requests.

    Args:
        __package (str): __package, keyword you want to search for.

    Return:
        dict. A dict with an entry for each CVE with these keyword : ID,URL,DESC.

    Examples:
    
    * Example for a simple __package request::

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
    
    base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=" + __package # __package can be a keyword or a CVE ID or a list of Keyword/CVE ID (separate with a +) 
    document = lh.fromstring(requests.get(base_url).text) 
    cve_entries = document.cssselect("div#TableWithRules table tr > td") # List of <tr> entries for CVE in main page

    for i in range(0, len(cve_entries) , 2):
        dictMain[id] = {
            "__PACKAGE" : __package,
            "ID"   : cve_entries[i].text_content(),
            "URL"  : "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_entries[i].text_content(),
            "DESC" : cve_entries[i+1].text_content().strip()
        }
        id +=1

    return dictMain

def get_cve_detail(cve_simple):
    """Main function to get cve **details**

    Get all the CVE details for a package/keyword. These are valid string:

    * Make multiple package request at the same time : ``get_cve_detail("package1,package2")``
    * Use several keyword to narrow a research : ``get_cve_detail("keyword1+keyword2)"``
    * And a combination of the above options : ``get_cve_detail("keyword1+keyword2,package1,package2")``. Here there will be 3 differents requests.

    Args:
        __package (str): __package, keyword you want to search for.

    Return:
        dict. A dict with an entry for each CVE with these keyword : ID,URL,DESC,NVD_URL,CNA,CVE_REF_URL.

    Examples:

    * Example for a simple __package request::

        >> crawler.get_cve_detail("jython")
        {
            0: {
                'ID' : 'CVE-2016-4000',
                'DESC' : 'Jython before 2.7.1rc1 allows attackers to execute arbitrary code via a '
                'crafted serialized PyFunction object.', # cve description
                'NVD_URL' : 'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-4000',
                'CNA' : 
                'CVE_REF_URL' : [
                 'http://advisories.mageia.org/MGASA-2015-0096.html',
                 'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
                 'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
                 'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
                 'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html'
                ]
            },
            1: {
                'ID' : 'CVE-2013-2027',
                'DESC' : 'Jython 2.2.1 uses the current umask to set the privileges of the class '
                'cache files, which allows local users to bypass intended access '
                'restrictions via unspecified vectors.',
                'NVD_URL' : 'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-2027',
                'CVE_REF_URL' : [
                 'http://advisories.mageia.org/MGASA-2015-0096.html',
                 'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
                 'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
                 'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
                 'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html'
                ]
            }
        }
    """
    cve_detail = {}

    for id, cve in cve_simple.items(): 
        details = get_detail(cve["URL"])

        cve_detail[id] = {
            "ID"   : cve_simple[id]["ID"],
            "DESC" : cve_simple[id]["DESC"],
            "NVD_URL" :  details["NVD_URL"],
            "CNA" : details["CNA"],
            "RELEASE_DATE" :details["RELEASE_DATE"],
            "CVE_REF_URL" :details["CVE_REF_URL"]
        }

    return cve_detail 


def get_detail(url):
    results = {}
    # Add name, description and more like the non-optimized one
    document = lh.fromstring(requests.get(url, stream=True).text)  
    
    # SELECTOR
    ## Reference Selector -> reference link and source
    ref_selector = document.cssselect("div#GeneratedTable table tr td ul li a")

    cve_ref = [c.get("href") for c in ref_selector]
    results["CVE_REF_URL"] = cve_ref

    ## NVD Selector
    nvd_selector = document.cssselect("div#GeneratedTable .ltgreybackground a")
    nvd_link = nvd_selector[0].get("href")
    results["NVD_URL"] = nvd_link

    ## Assigning CNA Selector
    cna_selector = document.cssselect("div#GeneratedTable table tr:nth-child(9)")
    cna = cna_selector[0].text_content().strip()
    results["CNA"] = cna

    ## Date entry Selector
    date_selector = document.cssselect("div#GeneratedTable table tr:nth-child(11) td b")
    date = date_selector[0].text_content()
    date = date[0:4] + "/" + date[4:6] + "/" + date[6:]
    results["RELEASE_DATE"] = date

    return results