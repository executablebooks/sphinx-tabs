#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as readme:
    long_description = readme.read()
long_description += '\n\n'
with open('CHANGES.txt') as changes:
    long_description += changes.read()


setup(
    name = 'sphinx-tabs',
    version = '1.1.13',
    author = 'djungelorm',
    author_email = 'djungelorm@users.noreply.github.com',
    packages = ['sphinx_tabs', 'sphinx_tabs.test'],
    test_suite='sphinx_tabs.test',
    package_data = {
        'sphinx_tabs': [
            'tabs.js',
            'tabs.css',
            'semantic-ui-2.4.1/*',
        ],
    },
    data_files = [("", ["LICENSE"])],
    url = 'https://github.com/djungelorm/sphinx-tabs',
    license = 'MIT',
    description = 'Tab views for Sphinx',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = ['sphinx>=1.4'],
    tests_require = ['sphinx>=1.4', 'docutils', 'pygments', 'sphinx_testing', 'lxml'],
    python_requires = '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ]
)
