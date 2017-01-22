""" Tabbed views for Sphinx, with HTML builder """

import os
from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx.util.osutil import copyfile

FILES = [
    'tabs.js',
    'jquery-ui.min.js',
    'jquery-ui.min.css'
]


class TabsDirective(Directive):
    """ Top-level tabs directive """

    has_content = True

    def run(self):
        """ Parse a tabs directive """
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nodes.container()
        node['classes'].append('tabs')
        self.add_name(node)

        env.temp_data['tabs_titles'] = []
        titles = nodes.bullet_list()
        node += titles

        self.state.nested_parse(self.content, self.content_offset, node)

        for tab_id, title in env.temp_data['tabs_titles']:
            item = nodes.list_item()
            para = nodes.paragraph()
            ref = nodes.reference('', '')
            ref['refuri'] = '#'+tab_id
            ref += nodes.Text(title)
            para += ref
            item += para
            titles += item
        return [node]


class TabDirective(Directive):
    """ Tab directive, for adding a tab to a collection of tabs """

    has_content = True

    def run(self):
        """ Parse a tab directive """
        env = self.state.document.settings.env
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.container(text)

        tab_id = "tab-%d" % env.new_serialno('tab')
        node['ids'].append(tab_id)
        env.temp_data['tabs_titles'].append((tab_id, self.content[0]))

        node['classes'].append('tab')
        self.add_name(node)
        self.state.nested_parse(self.content[2:], self.content_offset, node)
        return [node]


def add_assets(app):
    """ Add CSS and JS asset files """
    for path in FILES:
        if '.css' in path:
            app.add_stylesheet(path)
        elif '.js' in path:
            app.add_javascript(path)


def copy_assets(app, exception):
    """ Copy asset files to the output """
    if app.builder.name != 'html' or exception:
        return
    app.info('Copying tabs assets... ', nonl=True)
    for path in FILES:
        dest = os.path.join(app.builder.outdir, '_static', path)
        source = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
        copyfile(source, dest)
    app.info('done')


def setup(app):
    """ Set up the plugin """
    app.add_directive('tabs', TabsDirective)
    app.add_directive('tab', TabDirective)
    app.connect('builder-inited', add_assets)
    app.connect('build-finished', copy_assets)
