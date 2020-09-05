import pytest

@pytest.mark.parametrize("docname", ["index", "other", "other2"])
@pytest.mark.sphinx(testroot='conditionalassets')
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
        assert check_asset_links(app, docname)
    else:
        assert check_asset_links(app, docname, present=False)
