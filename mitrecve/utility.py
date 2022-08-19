def print_vulnerabilites(simple_cve):
    for cve in simple_cve.values():
        print("\nCVE :"       ,  cve["ID"])
        print("CVE URL :"     ,  cve["URL"]) 
        print("DESCRIPTION :" ,  cve["DESC"])


def print_vulnerabilites_detail(details_cve):
    for cve in details_cve.values() : 
        print("CVE :"           ,cve["ID"]) 
        print("DESCRIPTION :"   ,cve["DESC"]) 
        print("NVD LINK :"      ,cve["NVD_URL"]) 
        print("CNA :"           ,cve["CNA"])
        print("RELEASE DATE :"  ,cve["RELEASE_DATE"])
        print("\nReference for CVE:", cve["ID"])
        for ref_links in cve["CVE_REF_URL"] :
            print("\tCVE REFERENCE :" , ref_links)
        print("\n")