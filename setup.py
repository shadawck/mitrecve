#!/usr/bin/env python3

import pathlib
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="mitrecve",
    version="1.0.1",
    description="Get all cve corresponding to a specific keyword or a list of keywords - Packages or products for example - from the mitre website Display or save these informations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remiflavien1/mitrecve",
    author="shadawck",
    author_email="hug211mire@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["mitrecve"],
    include_package_data=True,   
    install_requires=["requests", "docopt", "beautifulsoup4"],
    entry_points={
        "console_scripts": [
            "mitrecve=mitrecve.__main__:main",
        ]
    },
)