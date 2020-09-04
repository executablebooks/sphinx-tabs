import pytest

@pytest.mark.sphinx(testroot='basic')
def test_build_html(
    app,
    status,
    warning,
    check_build_success,
    get_sphinx_app_output,
    get_sphinx_app_doctree
    ):
    app.build()
    check_build_success(status, warning)
    get_sphinx_app_doctree(app, regress=True)
    get_sphinx_app_output(app, regress=True)
