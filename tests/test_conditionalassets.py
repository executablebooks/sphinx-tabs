import pytest


@pytest.mark.parametrize("docname", ["index", "no_tabs1", "no_tabs2"])
@pytest.mark.sphinx(testroot="conditionalassets")
def test_build_html(
    app,
    status,
    warning,
    docname,
    check_build_success,
    get_sphinx_app_output,
    get_sphinx_app_doctree,
    check_asset_links,
):
    app.build()
    check_build_success(status, warning)
    get_sphinx_app_doctree(app, docname=docname, regress=True)
    get_sphinx_app_output(app, filename=docname + ".html", regress=True)

    if docname == "index":
        check_asset_links(app)
    else:
        check_asset_links(app, filename=docname + ".html", present=False)
