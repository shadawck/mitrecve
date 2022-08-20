# MITRECVE  

[![PyPI version](https://badge.fury.io/py/mitrecve.svg)](https://badge.fury.io/py/mitrecve) [![Requirements Status](https://requires.io/github/shadawck/mitrecve/requirements.svg?branch=master)](https://requires.io/github/shadawck/mitrecve/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/shadawck/badge/?version=latest)](https://mitrecve.readthedocs.io/en/latest/?badge=latest)

Get all CVE corresponding to a specific keyword or list of keywords from the [MITRE](https://cve.mitre.org/) database.

For a complete documentation look at [ReadTheDocs](https://mitrecve.readthedocs.io/en/latest/)

## Install

You can install ```mitrecve``` either via pip (PyPI) or from source.
To install using pip:

```bash
python3 -m pip install mitrecve
```

Or manually:

```sh
git clone https://github.com/remiflavien1/mitrecve
cd mitrecve
python3 setup.py install
# Or
python3 -m pip install .
```

## CLI

```sh
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
```

Example of output for the python ```html5lib``` module:

```sh
mitrecve crawl html5lib
```

```sh
-------------- Package: <html5lib>  --------------

CVE : CVE-2016-9910
CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9910
DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of special characters in attribute values, a different vulnerability than CVE-2016-9909.


CVE : CVE-2016-9909
CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9909
DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of the < (less than) character in attribute values.
```

You can also search for multiple keywords and print (and/or save with ```-o,--output``` flag) additional details with  ```--detail``` flag:

```sh
mitrecve crawl recon-ng,harvester --detail
```

```sh
CVE : CVE-2018-20752
DESCRIPTION : An issue was discovered in Recon-ng before 4.9.5. Lack of validation in the modules/reporting/csv.py file allows CSV injection. More specifically, when a Twitter user possesses an Excel macro for a username, it will not be properly sanitized when exported to a CSV file. This can result in remote code execution for the attacker.
NVD LINK : https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2018-20752
CNA : MITRE Corporation
RELEASE DATE : 2019/02/04

Reference for CVE: CVE-2018-20752
        CVE REFERENCE : https://bitbucket.org/LaNMaSteR53/recon-ng/commits/41e96fd58891439974fb0c920b349f8926c71d4c#chg-modules/reporting/csv.py
        CVE REFERENCE : https://bitbucket.org/LaNMaSteR53/recon-ng/issues/285/csv-injection-vulnerability-identified-in



-------------- Package: <harvester> --------------
CVE : CVE-2011-5197
DESCRIPTION : Cross-site request forgery (CSRF) vulnerability in index/manager/fileUpload in Public Knowledge Project Open Harvester Systems 2.3.1 and earlier allows remote attackers to hijack the authentication of administrators for requests that upload PHP files.
NVD LINK : https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-5197
CNA : MITRE Corporation
RELEASE DATE : 2012/09/23

Reference for CVE: CVE-2011-5197
        CVE REFERENCE : http://www.exploit-db.com/exploits/18266

```

# API

Just import and use it.

```python
>>> from mitrecve import crawler
>>> from pprint import pprint

>>> cve_simple = crawler.get_main_page("jython") 
>>> pprint(cve_simple)
```

```yaml
{0: {'DESC': 'Jython before 2.7.1rc1 allows attackers to execute arbitrary '
             'code via a crafted serialized PyFunction object.',
     'ID': 'CVE-2016-4000',
     'URL': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4000',
     '__PACKAGE': 'jython'},
 1: {'DESC': 'Jython 2.2.1 uses the current umask to set the privileges of the '
             'class cache files, which allows local users to bypass intended '
             'access restrictions via unspecified vectors.',
     'ID': 'CVE-2013-2027',
     'URL': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-2027',
     '__PACKAGE': 'jython'}}
```

# cve detail

```python
>>> pprint(crawler.get_cve_detail(cve_simple))
```

```yaml
{0: {'CNA': 'MITRE Corporation',
     'CVE_REF_URL': ['http://www.securityfocus.com/bid/105647',
                     'http://bugs.jython.org/issue2454',
                     'http://www.oracle.com/technetwork/security-advisory/cpuoct2018-4428296.html',
                     'https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=864859',
                     'https://hg.python.org/jython/file/v2.7.1rc1/NEWS',
                     'https://hg.python.org/jython/rev/d06e29d100c0',
                     'https://www.oracle.com/technetwork/security-advisory/cpujan2019-5072801.html',
                     'http://www.debian.org/security/2017/dsa-3893',
                     'https://security.gentoo.org/glsa/201710-28',,
                     'https://security-tracker.debian.org/tracker/CVE-2016-4000',
                     'https://snyk.io/vuln/SNYK-JAVA-ORGPYTHON-31451',
                     'https://www.oracle.com/security-alerts/cpuapr2020.html',
                     'https://www.oracle.com/technetwork/security-advisory/cpuapr2019-5072813.html',
                     'https://www.oracle.com/technetwork/security-advisory/cpuoct2019-5072832.html',
                     'https://lists.apache.org/thread.html/0919ec1db20b1022f22b8e78f355667df74d6142b463ff17d03ad533@%3Cdevnull.infra.apache.org%3E'],
     'DESC': 'Jython before 2.7.1rc1 allows attackers to execute arbitrary '
             'code via a crafted serialized PyFunction object.',
     'ID': 'CVE-2016-4000',
     'NVD_URL': 'https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-4000',
     'RELEASE_DATE': '2016/04/12'},
 1: {'CNA': 'Red Hat, Inc.',
     'CVE_REF_URL': ['http://advisories.mageia.org/MGASA-2015-0096.html',
                     'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
                     'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
                     'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
                     'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html'],
     'DESC': 'Jython 2.2.1 uses the current umask to set the privileges of the '
             'class cache files, which allows local users to bypass intended '
             'access restrictions via unspecified vectors.',
     'ID': 'CVE-2013-2027',
     'NVD_URL': 'https://nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-2027',
     'RELEASE_DATE': '2013/02/19'}}
```

## Troubleshooting

### Lxml not found ( python <= 3.6 )

Make sure pip resolve all the dependencies. If not working install package manually :

```sh
pip3 install lxml cssselect
```
