CLI Examples 
=============

Help 
-----

When you invoke ``mitrecve`` without flag you will be prompted basic available command.

.. code-block:: sh

    >> mitrecve
    Basic usage:
      mitrecve <package> [--verbose --detail ] [-o FILE]
      mitrecve ( -h | --help | --version )

Use ``--help`` flag to get all optionals arguments.

.. code-block:: sh
    
    >> mitrecve --help
    MitreCVE

    Basic usage:
      mitrecve <package> [--verbose --detail ] [-o FILE]
      mitrecve ( -h | --help | --version )

    options:
      -v --verbose      Show full output.
      -d --detail       Show CVE details.
      -o --output FILE   Save output to file.
      -h --help         Show this screen.
         --version      Show version.

Requesting CVE
---------------

For searching you have differents options.

1. Searching by Keyword/Packages
.................................

Search on Mitre all the CVE with the ``Package`` occurence.

.. code-block:: sh 

  >> mitrecve <packages/keywords>

.. code-block:: sh 
  :caption: Example: Request for all CVE in relation with the ``html5lib`` packages

  >> mitrecve html5lib
  -------------- Package: <html5lib> --------------

  CVE : CVE-2016-9910
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9910
  DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of special characters in attribute values, a different vulnerability than CVE-2016-9909.
  
  CVE : CVE-2016-9909
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9909
  DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of the < (less than) character in attribute values.

You can also **search for multiple keywords** to narrow your result by adding a plus between keywords: 

.. code-block:: sh
  :caption: Example: Request for all CVE in relation with ``Cisco`` products and who make them crash: 

  >> mitrecve cisco+crash
  CVE : CVE-2020-3353
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-3353
  DESCRIPTION A vulnerability in the syslog processing engine of Cisco Identity Services Engine (ISE) could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device. The vulnerability is due to a race condition that may occur when syslog messages are processed. An attacker could exploit this vulnerability by sending a high rate of syslog messages to an affected device. A successful exploit could allow the attacker to cause the Application Server process to crash, resulting in a DoS condition.

  CVE : CVE-2020-3344
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-3344
  DESCRIPTION A vulnerability in Cisco AMP for Endpoints Linux Connector Software and Cisco AMP for Endpoints Mac Connector Software could allow an authenticated, local attacker to cause a buffer overflow on an affected device. The vulnerability is due to insufficient input validation. An attacker could exploit this vulnerability by sending a crafted packet to an affected device. A successful exploit could allow the attacker to cause the Cisco AMP for Endpoints service to crash and restart.

  ... <SNIP> ...

  CVE : CVE-2000-0984
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2000-0984
  DESCRIPTION The HTTP server in Cisco IOS 12.0 through 12.1 allows local users to cause a denial of service (crash and reload) via a URL containing a "?/" string.
  
  CVE : CVE-1999-0159
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1999-0159
  DESCRIPTION Attackers can crash a Cisco IOS router or device, provided they can get to an interactive prompt (such as a login).  This applies to some IOS 9.x, 10.x, and 11.

You can also search individually (or not) for differents packages/keywords at the same type by adding a comma between keywords/packages.

.. code-block:: sh 

  >> mitrecve winrm,bloodhound
  
  >>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE <<<<<<<<<<<<<<<
  -------------- Package: <winrm> --------------
  CVE : CVE-2018-11746
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11746
  DESCRIPTION In Puppet Discovery prior to 1.2.0, when running Discovery against Windows hosts, WinRM connections can fall back to using basic auth over insecure channels if a HTTPS server is not available. This can expose the login credentials being used by Puppet Discovery.


  CVE : CVE-2007-1658
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-1658
  DESCRIPTION Windows Mail in Microsoft Windows Vista might allow user-assisted remote attackers to execute certain programs via a link to a (1) local file or (2) UNC share pathname in which there is a directory with the same base name as an executable program at the same level, as demonstrated using C:/windows/system32/winrm (winrm.cmd) and migwiz (migwiz.exe).

  -------------- Package: <bloodhound> --------------
  CVE : CVE-2019-15701
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-15701
  DESCRIPTION components/Modals/HelpModal.jsx in BloodHound 2.2.0 allows remote attackers to execute arbitrary OS commands (by spawning a child process as the current user on the victim's machine) when the search function's autocomplete feature is used. The victim must import data from an Active Directory with a GPO containing JavaScript in its name.


2. Searching by ID
.....................
If you know the CVE ID number, search by the number to find its description

.. code-block:: sh 

  >> mitrecve CVE-2020-9472

  >>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE <<<<<<<<<<<<<<<
  
  -------------- Package: <CVE-2020-9472> --------------
  CVE : CVE-2020-9472
  CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-9472
  DESCRIPTION Umbraco CMS 8.5.3 allows an authenticated file upload (and consequently Remote Code Execution) via the Install Package functionality.

3. Details
............

Add ``--detail``  flag for all the aboves requests to get more informations like **Reference Links** (Sources & Exploits), **NVD link** (and soon : CNA, creation Date, Exploit Code ...)

.. code-block:: sh

  >> mitrecve 2020-2555 --detail
  
  CVE : CVE-2020-2555
  DESCRIPTION : Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Caching,CacheStore,Invocation). Supported versions that are affected are 3.7.1.0, 12.1.3.0.0, 12.2.1.3.0 and 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3 to compromise Oracle Coherence. Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.0 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).


  NVD LINK : https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2020-2555

  Reference for CVE: CVE-2020-2555
  	CVE REFERENCE : http://packetstormsecurity.com/files/157054/Oracle-Coherence-Fusion-Middleware-Remote-Code-Execution.html
  	CVE REFERENCE : http://packetstormsecurity.com/files/157207/Oracle-WebLogic-Server-12.2.1.4.0-Remote-Code-Execution.html
  	CVE REFERENCE : http://packetstormsecurity.com/files/157795/WebLogic-Server-Deserialization-Remote-Code-Execution.html
  	CVE REFERENCE : https://www.oracle.com/security-alerts/cpujan2020.html