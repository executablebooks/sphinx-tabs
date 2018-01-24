# pylint: disable=import-error,no-name-in-module
from distutils.version import StrictVersion
# pylint: enable=import-error,no-name-in-module
from io import StringIO
import unittest
import re
import pkg_resources
from lxml import etree
from sphinx import __version__ as __sphinx_version__
from sphinx.builders.html import StandaloneHTMLBuilder


def _parse(xml):
    xml = xml.replace('&copy;', 'copy_sym')
    parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
    return etree.parse(StringIO(xml), parser)


def _strip_xmlns(xml):
    return xml.replace(' xmlns="http://www.w3.org/1999/xhtml"', '')


def get_scripts(xml):
    tree = _parse(xml)
    scripts = tree.findall('.//{*}script')
    scripts = [x.get('src') for x in scripts]
    return [x.replace('_static/', '') for x in scripts if x is not None]


def get_stylesheets(xml):
    tree = _parse(xml)
    stylesheets = tree.findall('.//{*}link[@rel="stylesheet"]')
    return [x.get('href').replace('_static/', '') for x in stylesheets]


def get_body(xml):
    tree = _parse(xml)
    body = tree.find('.//{*}div[@class="bodywrapper"]')[0][0]
    return _strip_xmlns(etree.tostring(body).decode('utf-8'))


def normalize_xml(xml):
    content = re.sub(r'>\s+<', '><', xml)
    content = etree.tostring(
        _parse(content), pretty_print=True).decode('utf-8')
    return content


class TestCase(unittest.TestCase):
    def tearDown(self):  # pylint: disable=invalid-name
        # Reset script and css files after test
        StandaloneHTMLBuilder.script_files = \
            StandaloneHTMLBuilder.script_files[:3]
        if StrictVersion(__sphinx_version__) > StrictVersion('1.6.0'):
            # pylint: disable=no-name-in-module
            from sphinx.builders.html import CSSContainer
            StandaloneHTMLBuilder.css_files = CSSContainer()
            # pylint: enable=no-name-in-module
        else:
            StandaloneHTMLBuilder.css_files = []

    @staticmethod
    def get_result(app, filename):
        return (app.outdir / (filename+'.html')).read_text(encoding='utf-8')

    @staticmethod
    def get_expectation(dirname, filename):
        return pkg_resources.resource_string(
            __name__, '%s/%s.html' % (dirname, filename)).decode('utf-8')

    def assertXMLEqual(  # pylint: disable=invalid-name
            self, expected, actual):
        expected = normalize_xml(expected)
        actual = normalize_xml(get_body(actual))
        self.assertEqual(expected, actual)

    def assertHasTabsAssets(  # pylint: disable=invalid-name
            self, xml, filter_scripts=None):
        stylesheets = get_stylesheets(xml)
        scripts = get_scripts(xml)
        if filter_scripts is not None:
            scripts = [x for x in scripts if filter_scripts(x)]
        self.assertEqual(stylesheets, [
            'alabaster.css',
            'pygments.css',
            'sphinx_tabs/tabs.css',
            'sphinx_tabs/semantic-ui-2.2.10/segment.min.css',
            'sphinx_tabs/semantic-ui-2.2.10/menu.min.css',
            'sphinx_tabs/semantic-ui-2.2.10/tab.min.css',
            'custom.css'
        ])
        self.assertEqual(scripts, [
            'jquery.js',
            'underscore.js',
            'doctools.js',
            'sphinx_tabs/tabs.js',
            'sphinx_tabs/semantic-ui-2.2.10/tab.min.js'
        ])

    def assertDoesNotHaveTabsAssets(  # pylint: disable=invalid-name
            self, xml):
        stylesheets = get_stylesheets(xml)
        scripts = get_scripts(xml)
        self.assertEqual(stylesheets, [
            'alabaster.css',
            'pygments.css',
            'custom.css'
        ])
        self.assertEqual(scripts, [
            'jquery.js',
            'underscore.js',
            'doctools.js'
        ])

    def assertStylesheetsEqual(  # pylint: disable=invalid-name
            self, expected, xml):
        actual = get_stylesheets(xml)
        self.assertEqual(expected, actual)

    def assertScriptsEqual(  # pylint: disable=invalid-name
            self, expected, xml):
        actual = get_scripts(xml)
        self.assertEqual(expected, actual)
