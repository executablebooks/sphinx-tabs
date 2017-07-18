from setuptools import setup

setup(
    name = 'sphinx-tabs',
    version = '1.0.1',
    author = 'djungelorm',
    author_email = 'djungelorm@users.noreply.github.com',
    packages = ['sphinx_tabs'],
    package_data = {
        'sphinx_tabs': [
            'tabs.js',
            'tabs.css',
            'semantic-ui-2.2.10/*',
        ],
    },
    url = 'https://github.com/djungelorm/sphinx-tabs',
    license = 'MIT',
    description = 'Tab views for Sphinx',
    install_requires = ['sphinx>=1.2'],
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ]
)
