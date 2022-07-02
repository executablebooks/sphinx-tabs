from os import path
import re
from setuptools import setup


def get_version():
    text = open(path.join(path.dirname(__file__), "sphinx_tabs", "__init__.py")).read()
    match = re.compile(r"^__version__\s*\=\s*[\"\']([^\s\'\"]+)", re.M).search(text)
    return match.group(1)


with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="sphinx-tabs",
    version=get_version(),
    description="Tabbed views for Sphinx",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="djungelorm",
    author_email="djungelorm@users.noreply.github.com",
    packages=["sphinx_tabs"],
    include_package_data=True,
    url="https://github.com/executablebooks/sphinx-tabs",
    license="MIT",
    python_requires="~=3.7",
    install_requires=["sphinx", "pygments", "docutils~=0.18.0"],
    extras_require={
        "testing": [
            "coverage",
            "pytest>=7.1,<8",
            "pytest-cov",
            "pytest-regressions",
            "pygments",
            "sphinx_testing",
            "bs4",
            "rinohtype",
        ],
        "code_style": ["pre-commit==2.13.0"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
