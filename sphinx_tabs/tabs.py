""" Tabbed views for Sphinx, with HTML builder """

import base64
from pathlib import Path
from functools import partial

from docutils import nodes
from docutils.parsers.rst import directives
from pkg_resources import resource_filename
from pygments.lexers import get_all_lexers
from sphinx.highlighting import lexer_classes
from sphinx.util.osutil import copyfile
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.directives.code import CodeBlock


FILES = [
    "semantic-ui-2.4.1/segment.min.css",
    "semantic-ui-2.4.1/menu.min.css",
    "semantic-ui-2.4.1/tab.min.css",
    "semantic-ui-2.4.1/tab.min.js",
    "tabs.js",
    "tabs.css",
]


LEXER_MAP = {}
for lexer in get_all_lexers():
    for short_name in lexer[1]:
        LEXER_MAP[short_name] = lexer[0]


def get_compatible_builders(app):
    builders = [
        "html",
        "singlehtml",
        "dirhtml",
        "readthedocs",
        "readthedocsdirhtml",
        "readthedocssinglehtml",
        "readthedocssinglehtmllocalmedia",
        "spelling",
    ]
    builders.extend(app.config["sphinx_tabs_valid_builders"])
    return builders


class TabsDirective(SphinxDirective):
    """ Top-level tabs directive """

    has_content = True

    def run(self):
        """ Parse a tabs directive """
        self.assert_has_content()

        node = nodes.container()
        node["classes"] = ["sphinx-tabs"]

        if "next_tabs_id" not in self.env.temp_data:
            self.env.temp_data["next_tabs_id"] = 0
        if "tabs_stack" not in self.env.temp_data:
            self.env.temp_data["tabs_stack"] = []

        tabs_id = self.env.temp_data["next_tabs_id"]
        tabs_key = "tabs_%d" % tabs_id
        self.env.temp_data["next_tabs_id"] += 1
        self.env.temp_data["tabs_stack"].append(tabs_id)

        self.env.temp_data[tabs_key] = {}
        self.env.temp_data[tabs_key]["tab_ids"] = []
        self.env.temp_data[tabs_key]["tab_titles"] = []
        self.env.temp_data[tabs_key]["is_first_tab"] = True

        self.state.nested_parse(self.content, self.content_offset, node)

        if self.env.app.builder.name in get_compatible_builders(self.env.app):
            tabs_node = nodes.container()
            tabs_node.tagname = "div"

            classes = "ui top attached tabular menu sphinx-menu"
            tabs_node["classes"] = classes.split(" ")

            tab_titles = self.env.temp_data[tabs_key]["tab_titles"]
            for idx, [data_tab, tab_name] in enumerate(tab_titles):
                tab = nodes.container()
                tab.tagname = "a"
                tab["classes"] = ["item"] if idx > 0 else ["active", "item"]
                tab["classes"].append(data_tab)
                tab += tab_name
                tabs_node += tab

            node.children.insert(0, tabs_node)

        self.env.temp_data["tabs_stack"].pop()
        return [node]


class TabDirective(SphinxDirective):
    """ Tab directive, for adding a tab to a collection of tabs """

    has_content = True

    def __init__(self, *args, **kwargs):
        self.tab_id = None
        self.tab_classes = set()
        super().__init__(*args, **kwargs)

    def run(self):
        """ Parse a tab directive """
        self.assert_has_content()

        tabs_id = self.env.temp_data["tabs_stack"][-1]
        tabs_key = "tabs_%d" % tabs_id

        include_tabs_id_in_data_tab = False
        if self.tab_id is None:
            tab_id = self.env.new_serialno(tabs_key)
            include_tabs_id_in_data_tab = True
        else:
            tab_id = self.tab_id

        tab_name = nodes.container()
        self.state.nested_parse(self.content[:1], self.content_offset, tab_name)

        i = 1
        while tab_id in self.env.temp_data[tabs_key]["tab_ids"]:
            tab_id = "%s-%d" % (tab_id, i)
            i += 1
        self.env.temp_data[tabs_key]["tab_ids"].append(tab_id)

        data_tab = str(tab_id)
        if include_tabs_id_in_data_tab:
            data_tab = "%d-%s" % (tabs_id, data_tab)
        data_tab = "sphinx-data-tab-{}".format(data_tab)

        self.env.temp_data[tabs_key]["tab_titles"].append((data_tab, tab_name))

        text = "\n".join(self.content)
        node = nodes.container(text)

        classes = "ui bottom attached sphinx-tab tab segment"
        node["classes"] = classes.split(" ")
        node["classes"].extend(self.tab_classes)
        node["classes"].append(data_tab)

        if self.env.temp_data[tabs_key]["is_first_tab"]:
            node["classes"].append("active")
            self.env.temp_data[tabs_key]["is_first_tab"] = False

        self.state.nested_parse(self.content[2:], self.content_offset, node)

        if self.env.app.builder.name not in get_compatible_builders(self.env.app):
            outer_node = nodes.container()
            tab = nodes.container()
            tab.tagname = "a"
            tab["classes"] = ["item"]
            tab += tab_name

            outer_node.append(tab)
            outer_node.append(node)
            return [outer_node]

        return [node]


class GroupTabDirective(TabDirective):
    """ Tab directive that toggles with same tab names across page"""

    has_content = True

    def run(self):
        self.assert_has_content()
        group_name = self.content[0]
        if self.tab_id is None:
            self.tab_id = base64.b64encode(group_name.encode("utf-8")).decode("utf-8")
        return super().run()


class CodeTabDirective(GroupTabDirective):
    """ Tab directive with a codeblock as its content"""

    has_content = True
    required_arguments = 1  # Lexer name
    optional_arguments = 1  # Custom label
    final_argument_whitespace = True
    option_spec = {  # From sphinx CodeBlock
        "force": directives.flag,
        "linenos": directives.flag,
        "dedent": int,
        "lineno-start": int,
        "emphasize-lines": directives.unchanged_required,
        "caption": directives.unchanged_required,
        "class": directives.class_option,
        "name": directives.unchanged,
    }

    def run(self):
        """ Parse a code-tab directive"""
        self.assert_has_content()

        if len(self.arguments) > 1:
            tab_name = self.arguments[1]
        elif self.arguments[0] in lexer_classes and not isinstance(
            lexer_classes[self.arguments[0]], partial
        ):
            tab_name = lexer_classes[self.arguments[0]].name
        else:
            try:
                tab_name = LEXER_MAP[self.arguments[0]]
            except:
                raise ValueError("Lexer not implemented: {}".format(self.arguments[0]))

        self.tab_classes.add("code-tab")

        # All content should be parsed as code
        code_block = CodeBlock.run(self)

        # Reset to generate tab node
        self.content.data = [tab_name, ""]
        self.content.items = [(None, 0), (None, 1)]

        node = super().run()
        node[0].extend(code_block)

        return node


class _FindTabsDirectiveVisitor(nodes.NodeVisitor):
    """Visitor pattern than looks for a sphinx tabs
    directive in a document"""

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self._found = False

    def unknown_visit(self, node):
        if (
            not self._found
            and isinstance(node, nodes.container)
            and "classes" in node
            and isinstance(node["classes"], list)
        ):
            self._found = "sphinx-tabs" in node["classes"]

    @property
    def found_tabs_directive(self):
        """ Return whether a sphinx tabs directive was found """
        return self._found


# pylint: disable=unused-argument
def update_context(app, pagename, templatename, context, doctree):
    """ Remove sphinx-tabs CSS and JS asset files if not used in a page """
    if doctree is None:
        return
    visitor = _FindTabsDirectiveVisitor(doctree)
    doctree.walk(visitor)
    if not visitor.found_tabs_directive:
        paths = [Path("_static") / "sphinx_tabs" / f for f in FILES]
        if "css_files" in context:
            context["css_files"] = context["css_files"][:]
            for path in paths:
                if path.suffix == ".css" and path in context["css_files"]:
                    context["css_files"].remove(path.as_posix())
        if "script_files" in context:
            context["script_files"] = context["script_files"][:]
            for path in paths:
                if path.suffix == ".js" and path.as_posix() in context["script_files"]:
                    context["script_files"].remove(path.as_posix())


# pylint: enable=unused-argument


def copy_assets(app, exception):
    """ Copy asset files to the output """
    if "getLogger" in dir(logging):
        log = logging.getLogger(__name__).info  # pylint: disable=no-member
        warn = logging.getLogger(__name__).warning  # pylint: disable=no-member
    else:
        log = app.info
        warn = app.warning
    builders = get_compatible_builders(app)
    if exception:
        return
    if app.builder.name not in builders:
        if not app.config["sphinx_tabs_nowarn"]:
            warn(
                "Not copying tabs assets! Not compatible with %s builder"
                % app.builder.name
            )
        return

    log("Copying tabs assets")

    installdir = Path(app.builder.outdir) / "_static" / "sphinx_tabs"

    for path in FILES:
        source = resource_filename("sphinx_tabs", path)
        dest = installdir / path

        destdir = dest.parent
        if not destdir.exists():
            destdir.mkdir(parents=True)

        copyfile(source, dest)


def setup(app):
    """ Set up the plugin """
    app.add_config_value("sphinx_tabs_nowarn", False, "")
    app.add_config_value("sphinx_tabs_valid_builders", [], "")
    app.add_directive("tabs", TabsDirective)
    app.add_directive("tab", TabDirective)
    app.add_directive("group-tab", GroupTabDirective)
    app.add_directive("code-tab", CodeTabDirective)
    for path in [Path("sphinx_tabs") / f for f in FILES]:
        if path.suffix == ".css":
            if "add_css_file" in dir(app):
                app.add_css_file(path.as_posix())
            else:
                app.add_stylesheet(path.as_posix())
        if path.suffix == ".js":
            if "add_script_file" in dir(app):
                app.add_script_file(path.as_posix())
            else:
                app.add_js_file(path.as_posix())
    app.connect("html-page-context", update_context)
    app.connect("build-finished", copy_assets)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
