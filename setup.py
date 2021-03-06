#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


deps = {
    'platon-keys': [
        "eth-utils>=1.3.0,<2.0.0",
    ],
    'test': [
        "asn1tools>=0.146.2,<0.147",
        "pyasn1>=0.4.5,<0.5",
        'pytest==3.2.2',
        'hypothesis==3.30.0',
        "eth-hash[pysha3];implementation_name=='cpython'",
        "eth-hash[pycryptodome];implementation_name=='pypy'",
    ],
    'lint': [
        'flake8==3.0.4',
        'mypy==0.701',
    ],
    'dev': [
        'tox==2.7.0',
        'bumpversion==0.5.3',
        'twine',
    ],
}

deps['dev'] = (
    deps['dev'] +
    deps['platon-keys'] +
    deps['lint'] +
    deps['test']
)

setup(
    name='platon-keys',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.1.0',
    description="""Common API for PlatON key operations.""",
    long_description_markdown_filename='README.md',
    author='awake006',
    author_email='hietel366435@gmail.com',
    url='https://github.com/awake006/platon-keys',
    include_package_data=True,
    setup_requires=['setuptools-markdown'],
    install_requires=deps['platon-keys'],
    py_modules=['platon_keys'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'platon-keys': ['py.typed']},
    keywords='platon',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
