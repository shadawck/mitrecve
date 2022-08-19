CLI Examples 
=============

Help 
-----

When you invoke ``mitrecve`` without flag you will be prompted basic available command.

.. code-block:: sh

    >> mitrecve
    usage:
      mitrecve crawl <package> [--detail ] [--format FORMAT]
      mitrecve show <result>
      mitrecve ( -h | --help | --version )

Use ``--help`` flag to get all optionals arguments.

.. code-block:: sh
    
    >> mitrecve --help
    MitreCVE

    Basic usage:
      mitrecve crawl <package> [--detail ] [--format FORMAT]
      mitrecve show <result>
      mitrecve ( -h | --help | --version )

    options:
        -f --format FORMAT   Choose output format (json)
        -d --detail          Show CVE details
        -h --help            Show this screen
           --version         Show version

Requesting CVE
---------------

For searching you have differents options.

1. Searching by Keyword/Packages
.................................

Search on Mitre all the CVE with the ``Package`` occurence.

.. code-block:: sh 

  >> mitrecve crawl <packages/keywords>

.. code-block:: sh 
  :caption: Example: Request for all CVE in relation with the ``html5lib`` packages

  >> mitrecve crawl html5lib
  -------------- Package: <html5lib> --------------

  CVE : CVE-2016-9910
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9910
  DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of special characters in attribute values, a different vulnerability than CVE-2016-9909.
  
  CVE : CVE-2016-9909
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9909
  DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of the < (less than) character in attribute values.

You can also **search for multiple keywords** to narrow your result by adding a plus between keywords: 

.. code-block:: sh
  :caption: Example: Request for all CVE in relation with ``Cisco`` products with the "crash" keyword: 

  >> mitrecve crawl cisco+crash
  -------------- Package: <cisco+crash> --------------
  CVE : CVE-2022-20792
  CVE URL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-20792
  DESCRIPTION A vulnerability in the regex module used by the signature database load module of Clam AntiVirus (ClamAV) versions 0.104.0 through 0.104.2 and LTS version 0.103.5 and prior versions could allow an authenticated, local attacker to crash ClamAV at database load time, and possibly gain code execution. The vulnerability is due to improper bounds checking that may result in a multi-byte heap buffer overwflow write. An attacker could exploit this vulnerability by placing a crafted CDB ClamAV signature database file in the ClamAV database directory. An exploit could allow the attacker to run code as the clamav user.

  CVE : CVE-2022-20748
  CVE URL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-20748
  DESCRIPTION A vulnerability in the local malware analysis process of Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on the affected device. This vulnerability is due to insufficient error handling in the local malware analysis process of an affected device. An attacker could exploit this vulnerability by sending a crafted file through the device. A successful exploit could allow the attacker to cause the local malware analysis process to crash, which could result in a DoS condition. Notes: Manual intervention may be required to recover from this situation. Malware cloud lookup and dynamic analysis will not be impacted.
  
  ... <SNIP> ...

  CVE : CVE-2022-20792
  CVE URL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-20792
  DESCRIPTION A vulnerability in the regex module used by the signature database load module of Clam AntiVirus (ClamAV) versions 0.104.0 through 0.104.2 and LTS version 0.103.5 and prior versions could allow an authenticated, local attacker to crash ClamAV at database load time, and possibly gain code execution. The vulnerability is due to improper bounds checking that may result in a multi-byte heap buffer overwflow write. An attacker could exploit this vulnerability by placing a crafted CDB ClamAV signature database file in the ClamAV database directory. An exploit could allow the attacker to run code as the clamav user.

  CVE : CVE-2022-20748
  CVE URL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-20748
  DESCRIPTION A vulnerability in the local malware analysis process of Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on the affected device. This vulnerability is due to insufficient error handling in the local malware analysis process of an affected device. An attacker could exploit this vulnerability by sending a crafted file through the device. A successful exploit could allow the attacker to cause the local malware analysis process to crash, which could result in a DoS condition. Notes: Manual intervention may be required to recover from this situation. Malware cloud lookup and dynamic analysis will not be impacted.

You can also search individually (or not) for differents packages/keywords at the same type by adding a comma between keywords/packages.

.. code-block:: sh 

  >> mitrecve crawl winrm,bloodhound
  CVE : CVE-2021-27022
  CVE URL : https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-27022
  DESCRIPTION : A flaw was discovered in bolt-server and ace where running a task with sensitive parameters results in those sensitive parameters being logged when they should not be. This issue only affects SSH/WinRM nodes (inventory service nodes).

  CVE : CVE-2018-11746
  CVE URL : https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11746
  DESCRIPTION : In Puppet Discovery prior to 1.2.0, when running Discovery against Windows hosts, WinRM connections can fall back to using basic auth over insecure channels if a HTTPS server is not available. This can expose the login credentials being used by Puppet Discovery.

  CVE : CVE-2007-1658
  CVE URL : https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-1658
  DESCRIPTION : Windows Mail in Microsoft Windows Vista might allow user-assisted remote attackers to execute certain programs via a link to a (1) local file or (2) UNC share pathname in which there is a directory with the same base name as an executable program at the same level, as demonstrated using C:/windows/system32/winrm (winrm.cmd) and migwiz (migwiz.exe).

  -------------- Package: <bloodhound> --------------

  CVE : CVE-2021-3210
  CVE URL : https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3210
  DESCRIPTION : components/Modals/HelpTexts/GenericAll/GenericAll.jsx in Bloodhound <= 4.0.1 allows remote attackers to execute arbitrary system commands when the victim imports a malicious data file containing JavaScript in the objectId parameter.

  CVE : CVE-2019-15701
  CVE URL : https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-15701
  DESCRIPTION : components/Modals/HelpModal.jsx in BloodHound 2.2.0 allows remote attackers to execute arbitrary OS commands (by spawning a child process as the current user on the victim's machine) when the search function's autocomplete feature is used. The victim must import data from an Active Directory with a GPO containing JavaScript in its name.

2. Searching by ID
.....................
If you know the CVE ID number, search by the number to find its description

.. code-block:: sh 

  >> mitrecve crawl CVE-2020-9472
  -------------- Package: <CVE-2020-9472> --------------
  CVE : CVE-2020-9472
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-9472
  DESCRIPTION Umbraco CMS 8.5.3 allows an authenticated file upload (and consequently Remote Code Execution) via the Install Package functionality.

3. Details
............

Add ``--detail``  flag for all the aboves requests to get more informations like **Reference Links** (Sources & Exploits), **NVD link** (and soon : CNA, creation Date, Exploit Code ...)

.. code-block:: sh

  >> mitrecve crawl 2020-2555 --detail
  CVE : CVE-2020-2555
  DESCRIPTION : Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Caching,CacheStore,Invocation). Supported versions that are affected are 3.7.1.0, 12.1.3.0.0, 12.2.1.3.0 and 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3 to compromise Oracle Coherence. Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.0 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).
  NVD LINK : https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2020-2555
  CNA : Oracle
  RELEASE DATE : 2019/12/10

  Reference for CVE: CVE-2020-2555
          CVE REFERENCE : http://packetstormsecurity.com/files/157054/Oracle-Coherence-Fusion-Middleware-Remote-Code-Execution.html
          CVE REFERENCE : http://packetstormsecurity.com/files/157207/Oracle-WebLogic-Server-12.2.1.4.0-Remote-Code-Execution.html
          CVE REFERENCE : http://packetstormsecurity.com/files/157795/WebLogic-Server-Deserialization-Remote-Code-Execution.html

