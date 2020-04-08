"""
Get the vulnerabilities from different source (See docs/vuln-source.md) for each package found
"""
import json
import requests
from bs4 import BeautifulSoup

############################
##### CVE MITRE Source #####
############################
# https://cve.mitre.org/cve/search_cve_list.html

# No API but you can download the source in differents format XML, CSV ... but these are heavy file 
# It's more pratical to make little requests
# So let's go make a litle API with beautifulsoup and requests


def MITRE_get_main_page(package): 
    """
    Get all the CVE for a package/keyword
    """
    base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=" + package
    rq = requests.get(base_url).text

    # data struct : 
    # [(cve_name1, cve_link1, cve_desc1),...,(cve_name_n, cve_link_n, cve_desc_n)]
    cve_group = []
    soup = BeautifulSoup(rq, 'html.parser')


    # Get each line (cve_name/link, cve_description) from request rq in html format
    soup = soup.select("#TableWithRules")[0].find_all("tr") 

    souptd = []
    for el in soup : 
        souptd.append(el.find_all("td"))

    for td in souptd[1:] : 

        cve_group.append(
            (
                td[0].string.strip(), 
                 "https://cve.mitre.org" + td[0].a['href'],
                td[1].string.strip()
            )
        )
    return cve_group

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
