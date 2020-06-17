from mitrecve import crawler


def print_vulnerabilites(listDependencies, __verbose): 
    i = 0

    print("\n>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE <<<<<<<<<<<<<<<")

    for dep in listDependencies :
        list_vuln_by_dep = crawler.get_main_page(dep)

        if list_vuln_by_dep == [] : 
            if __verbose :
                print("\n-------------- Package: <" + listDependencies[i] + "> --------------")
                print("NO VULNERABILITIES FOUND")
            
            i += 1
            continue
        
        else :
            print("-------------- Package: <" + listDependencies[i] + "> --------------")
            i +=1

            # [(cve_name1, cve_link1, cve_desc1),...,(cve_name_n, cve_link_n, cve_desc_n)]
            for cve in list_vuln_by_dep : 
                print("CVE :"       ,  cve[0]) # print cve_name 
                print("CVE DETAIL"  ,  cve[1]) # print cve_link
                print("DESCRIPTION" ,  cve[2])

def print_vulnerabilites_detail(listDependencies,__verbose):
    
    # [(more_cve_1, [ref_1_cve_1, ref_2_cve_1]) ,..., (more_cve_n, [ref_1_cve_n, ref_2_cve_n])]
    i = 0

    print("\n>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE (Detail) <<<<<<<<<<<<<<<")
    for deps in listDependencies : 
        list_vuln_by_dep = crawler.get_cve_detail(deps)

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
                print("\nReference for CVE:", cve[0])
                for ref_links in cve[3] :
                    print("\tCVE REFERENCE :" , ref_links) # print cve_reference_links
                print("\n")

def print_vulnerabilites_detail_opti(listDependencies,__verbose):
    i = 0

    print("\n>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE (Detail) <<<<<<<<<<<<<<<")
    for deps in listDependencies : 
        list_vuln_by_dep = crawler.get_cve_detail_opti(deps)

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
                print("\nNVD Link:", cve[1])
                print("\nCNA:", cve[2])
                print("\nCreation Date:", cve[3],"\n")
                
                for ref_links in cve[0] :
                    print("CVE REFERENCE :" , ref_links) 
