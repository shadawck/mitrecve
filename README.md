# MITRECVE  

[![PyPI version](https://badge.fury.io/py/mitrecve.svg)](https://badge.fury.io/py/mitrecve) [![Requirements Status](https://requires.io/github/remiflavien1/mitrecve/requirements.svg?branch=master)](https://requires.io/github/remiflavien1/mitrecve/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/mitrecve/badge/?version=latest)](https://mitrecve.readthedocs.io/en/latest/?badge=latest)


Get all CVE corresponding to a specific keyword or list of keywords from the [MITRE](https://cve.mitre.org/) database.

For a complete documentation look at [ReadTheDocs](https://mitrecve.readthedocs.io/en/latest/)


# Install

You can install ```mitrecve``` either via pip (PyPI) or from source.
To install using pip:
```bash
python3 -m pip install mitrecve
```
Or manually:
```
git clone https://github.com/remiflavien1/mitrecve
cd mitrecve
python3 setup.py install
```

## CLI
```
mitrecve --help 

> mitrecve
> 
> usage:
>   mitrecve <package> [--verbose --detail ] [-o FILE]
>   mitrecve ( -h | --help | --version )
> 
> options:
>   -v --verbose      Show full output.
>   -d --detail       Show CVE details.
>   -o --output FILE   Save output to file.
>   -h --help         Show this screen.
>      --version      Show version.
```

Example of output for the python ```html5lib``` module:

```sh
mitrecve html5lib
```

```sh
>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE <<<<<<<<<<<<<<<

-------------- Package: <html5lib>  --------------

CVE : CVE-2016-9910
CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9910
DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of special characters in attribute values, a different vulnerability than CVE-2016-9909.


CVE : CVE-2016-9909
CVE DETAIL https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-9909
DESCRIPTION The serializer in html5lib before 0.99999999 might allow remote attackers to conduct cross-site scripting (XSS) attacks by leveraging mishandling of the < (less than) character in attribute values.
```

You can also search for multiple keywords and print (or save with ```-o,--output``` flag) additional details with  ```--detail``` flag: 
```sh
mitrecve recon-ng,harvester --detail
```

```sh
>>>>>>>>>>>>>>> SEARCH IN MITRE DATABASE (Detail) <<<<<<<<<<<<<<<

-------------- Package: <recon-ng> --------------

CVE : CVE-2018-20752
DESCRIPTION : An issue was discovered in Recon-ng before 4.9.5. Lack of validation in the modules/reporting/csv.py file allows CSV injection. More specifically, 
when a Twitter user possesses an Excel macro for a username, it will not be properly sanitized when exported to a CSV file. This can result in remote code execution for the attacker.
NVD LINK : http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2018-20752

 Reference for CVE: CVE-2018-20752
        CVE REFERENCE : https://bitbucket.org/LaNMaSteR53/recon-ng/commits/41e96fd58891439974fb0c920b349f8926c71d4c#chg-modules/reporting/csv.py
        CVE REFERENCE : https://bitbucket.org/LaNMaSteR53/recon-ng/issues/285/csv-injection-vulnerability-identified-in



-------------- Package: <harvester> --------------

CVE : CVE-2011-5197
DESCRIPTION : Cross-site request forgery (CSRF) vulnerability in index/manager/fileUpload in Public Knowledge Project Open Harvester Systems 2.3.1 and earlier allows remote attackers to hijack the authentication of administrators for requests that upload PHP files.
NVD LINK : http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-5197

 Reference for CVE: CVE-2011-5197
        CVE REFERENCE : http://www.exploit-db.com/exploits/18266
```

# API
Just import and use it.

```python
>>> from mitrecve import crawler
>>> from pprint import pprint

>>> pprint(crawler.get_main_page("jython"))
[('CVE-2016-4000',
  'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4000',
  'Jython before 2.7.1rc1 allows attackers to execute arbitrary code via a '
  'crafted serialized PyFunction object.'),
 ('CVE-2013-2027',
  'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-2027',
  'Jython 2.2.1 uses the current umask to set the privileges of the class '
  'cache files, which allows local users to bypass intended access '
  'restrictions via unspecified vectors.')]

# cve detail
>>> pprint(crawler.get_cve_detail("jython"))
[('CVE-2016-4000', # cve name
  'Jython before 2.7.1rc1 allows attackers to execute arbitrary code via a '
  'crafted serialized PyFunction object.', # cve description
  'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-4000', # nist detail
  ['http://advisories.mageia.org/MGASA-2015-0096.html',
   'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
   'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
   'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
   'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html']), # cve reference list
 ('CVE-2013-2027',
  'Jython 2.2.1 uses the current umask to set the privileges of the class '
  'cache files, which allows local users to bypass intended access '
  'restrictions via unspecified vectors.',
  'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-2027',
  ['http://advisories.mageia.org/MGASA-2015-0096.html',
   'http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html',
   'http://www.mandriva.com/security/advisories?name=MDVSA-2015:158',
   'https://bugzilla.redhat.com/show_bug.cgi?id=947949',
   'http://lists.opensuse.org/opensuse-updates/2015-02/msg00055.html'])]

```

## Troubleshooting 

### Lxml not found ( python <= 3.6 )

Make sure pip resolve all the dependencies. If not working install package manually : 
```sh 
pip3 install lxml cssselect
```
