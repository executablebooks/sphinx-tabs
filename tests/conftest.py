import os
import pytest
from pathlib import Path
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'roots'


@pytest.fixture
def check_build_success():
    def check(status, warning):
        assert "build succeeded" in status.getvalue()
        warnings = warning.getvalue().strip()
        assert warnings == ""

    return check
    
@pytest.fixture
def get_sphinx_app_output(file_regression):
    def read(
        app,
        buildername="html",
        filename="index.html",
        encoding="utf-8",
        regress=False,
        replace=None,
    ):
        outpath = path(os.path.join(str(app.srcdir), "_build", buildername, filename))
        if not outpath.exists():
            raise IOError("no output file exists: {}".format(outpath))

        try:
            # introduced in sphinx 3.0
            content = outpath.read_text(encoding=encoding)
        except AttributeError:
            content = outpath.text(encoding=encoding)

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
