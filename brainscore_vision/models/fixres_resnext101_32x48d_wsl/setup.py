#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = ["torchvision",
                "torch",
                "numpy",
                "importlib",
                "Fixing-the-train-test-resolution-discrepancy-scripts @ git+https://github.com/mschrimpf/FixRes.git"
                ]

setup(
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='brain-score template',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)