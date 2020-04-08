from mitrecve import crawler

# NEED OPTIMISATION ->    1 (ncall)    0.002    0.002    8.526 (cumtime)    8.526 (totime) /mnt/d/GIT/scabi/scabi/utility_cli.py:40(MITRE_print_vulnerabilites)
def MITRE_print_vulnerabilites(listDependencies, __verbose): 
    i = 0

    print("\n>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE <<<<<<<<<<<<<<<")

    for dep in listDependencies :
        list_vuln_by_dep = crawler.MITRE_get_main_page(dep)

        if list_vuln_by_dep == [] : 
            if __verbose :
                print("\n-------------- Package: <" + listDependencies[i] + "> --------------")
                print("NO VULNERABILITIES FOUND")
            
            i += 1
            continue
        
        else :
            print("\n-------------- Package: <" + listDependencies[i] + "> --------------\n")
            i +=1

            # [(cve_name1, cve_link1, cve_desc1),...,(cve_name_n, cve_link_n, cve_desc_n)]
            for cve in list_vuln_by_dep : 
                print("CVE :"       ,  cve[0]) # print cve_name 
                print("CVE DETAIL"  ,  cve[1]) # print cve_link
                print("DESCRIPTION" ,  cve[2]) # print cve_description
                print("\n")

def MITRE_print_vulnerabilites_detail(listDependencies,__verbose):
    
    # [(more_cve_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (more_cve_n, [ref_1_cve_n, ref_2_cve_n])]
    i = 0

    print("\n>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE (Detail) <<<<<<<<<<<<<<<")
    for deps in listDependencies : 
        list_vuln_by_dep = crawler.MITRE_get_cve_detail(deps)

        if list_vuln_by_dep == [] : 
            if __verbose :
                print("\n-------------- Package: <" + listDependencies[i] + "> --------------")
                print("NO VULNERABILITIES FOUND")

            i += 1
            continue
        
        else :
            print("\n-------------- Package: <" + listDependencies[i] + "> --------------\n")
            i +=1
            for cve in list_vuln_by_dep : 
                print("CVE :"           , cve[0]) # print cve_name 
                print("DESCRIPTION :"   , cve[1]) # print cve_description
                print("NVD LINK :"      , cve[2]) # print nvd_link
                print("\n Reference for CVE:", cve[0])
                for ref_links in cve[3] :
                    print("\tCVE REFERENCE :" , ref_links) # print cve_reference_links
                print("\n")

