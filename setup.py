from setuptools import setup

setup(
    name = 'sphinx-tabs',
    version = '0.1.0',
    author = 'djungelorm',
    author_email = 'djungelorm@users.noreply.github.com',
    packages = ['sphinx_tabs'],
    package_data = {'sphinx_tabs': ['tabs.js', 'jquery-ui.min.js', 'jquery-ui.min.css']},
    url = 'https://github.com/djungelorm/sphinx-tabs',
    license = 'MIT',
    description = 'Tab views for Sphinx',
    install_requires = ['Sphinx'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Documentation :: Sphinx'
    ]
)
