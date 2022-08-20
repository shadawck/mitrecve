#!/usr/bin/env python3

import pathlib
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="mitrecve",
    version="1.1.1",
    description="Get all CVE corresponding to a specific keyword or list of keywords from the MITRE database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadawck/mitrecve",
    author="shadawck",
    author_email="hug211mire@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["mitrecve"],
    include_package_data=True,   
    install_requires=required,
    entry_points={
        "console_scripts": [
            "mitrecve=mitrecve.__main__:main",
        ]
    },
)