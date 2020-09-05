import os
import pytest
from pathlib import Path
from sphinx.testing.path import path

from sphinx_tabs.tabs import FILES

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "roots"


@pytest.fixture
def check_build_success():
    """Check build is successful and there are no warnings."""

    def check(status, warning):
        assert "build succeeded" in status.getvalue()
        warnings = warning.getvalue().strip()
        assert warnings == ""

    return check


@pytest.fixture
def get_sphinx_app_output(file_regression):
    """Get sphinx HTML output and optionally regress."""

    def read(
        app,
        buildername="html",
        filename="index.html",
        encoding="utf-8",
        regress=False,
        replace=None,
    ):
        outpath = Path(app.srcdir) / "_build" / buildername / filename
        if not outpath.exists():
            raise IOError("No output file exists: {}".format(outpath.as_posix()))

        content = outpath.read_text(encoding=encoding)

        if regress:
            # only regress the inner body, since other sections are non-deterministic
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(content, "html.parser")
            doc_div = soup.findAll("div", {"class": "documentwrapper"})[0]
            text = doc_div.prettify()
            for find, rep in (replace or {}).items():
                text = text.replace(find, rep)
            file_regression.check(text, extension=".html", encoding="utf8")

        return content

    return read


@pytest.fixture
def get_sphinx_app_doctree(file_regression):
    """Get sphinx doctree and optionally regress."""

    def read(app, docname="index", resolve=False, regress=False, replace=None):
        if resolve:
            doctree = app.env.get_and_resolve_doctree(docname, app.builder)
            extension = ".resolved.xml"
        else:
            doctree = app.env.get_doctree(docname)
            extension = ".xml"

        # convert absolute filenames
        for node in doctree.traverse(lambda n: "source" in n):
            node["source"] = Path(node["source"]).name

        if regress:
            text = doctree.pformat()  # type: str
            for find, rep in (replace or {}).items():
                text = text.replace(find, rep)
            file_regression.check(text, extension=extension)

        return doctree

    return read


@pytest.fixture
def check_asset_links():
    """
    Check if all stylesheets and scripts (.js) have been referenced in HTML.
    Specify whether checking if assets are ``present`` or not ``present``.
    """

    def check(
        app, buildername="html", filename="index.html", encoding="utf-8", present=True
    ):
        outpath = Path(app.srcdir) / "_build" / buildername / filename
        if not outpath.exists():
            raise IOError("No output file exists: {}".format(outpath.as_posix()))

        content = outpath.read_text(encoding=encoding)

        from bs4 import BeautifulSoup

        css_assets = [f for f in FILES if f.endswith(".css")]
        js_assets = [f for f in FILES if f.endswith(".js")]

        soup = BeautifulSoup(content, "html.parser")
        stylesheets = soup.find_all("link", {"rel": "stylesheet"}, href=True)
        css_refs = [s["href"] for s in stylesheets]

        scripts = soup.find_all("script", src=True)
        js_refs = [s["src"] for s in scripts]

        all_refs = css_refs + js_refs

        if present:
            css_present = all(any(a in ref for ref in all_refs) for a in css_assets)
            js_present = all(any(a in ref for ref in js_refs) for a in js_assets)
            assert css_present
            assert js_present
        else:
            assert not "sphinx_tabs" in css_refs + js_refs

    return check
