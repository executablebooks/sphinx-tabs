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
        files=["index.html"],
        encoding="utf-8",
        regress=False
    ):
        contents = []

        for filename in files:
            outpath = path(os.path.join(str(app.srcdir), "_build", buildername, filename))
            if not outpath.exists():
                raise IOError("no output file exists: {}".format(outpath))
            header = "-"*len(filename) + "\n"
            title = header + f"{filename}\n" + header + "\n"
            doc = title + outpath.read_text(encoding=encoding)
            contents.append(doc)

        if regress:
            content = "\n".join(contents)
            file_regression.check(content, extension=".html")

        return content

    return read


@pytest.fixture
def get_sphinx_app_doctree(file_regression):
    def read(app, docname="index", resolve=False, regress=False):
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
            file_regression.check(doctree.pformat(), extension=extension)

        return doctree

    return read
