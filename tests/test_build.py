import pytest


@pytest.mark.sphinx(testroot="basic")
def test_basic():
    pass


@pytest.mark.sphinx(testroot="notabs")
def test_no_tabs(app, check_asset_links):
    check_asset_links(app, present=False)


@pytest.mark.parametrize("docname", ["index", "no_tabs1", "no_tabs2"])
@pytest.mark.sphinx(testroot="conditionalassets")
def test_conditional_assets(app, docname, check_asset_links):
    if docname == "index":
        check_asset_links(app)
    else:
        check_asset_links(app, filename=docname + ".html", present=False)


@pytest.mark.sphinx(testroot="linenos")
def test_other_with_assets(app, check_asset_links):
    check_asset_links(app)


@pytest.mark.sphinx(testroot="nestedmarkup")
def test_nested_markup(app, check_asset_links):
    check_asset_links(app)
