# sphinx-tabs

[![Github-CI][github-ci]][github-link]
[![Coverage Status][codecov-badge]][codecov-link]
[![PyPI][pypi-badge]][pypi-link]

Create tabbed content in [Sphinx documentation](http://www.sphinx-doc.org) when building HTML.

For example, see the [Raw] code of [docs/index.rst](docs/index.rst) which generates the following:

A live demo can be found here: <https://sphinx-tabs.readthedocs.io>

![Tabs](/images/tabs.gif)

## Installation

```bash
pip install sphinx-tabs
```

To enable the extension in Sphinx, add the following to your conf.py:

```python
extensions = ['sphinx_tabs.tabs']
```

If needed, there is a configuration option to allow additional builders to be considered compatible. For example, to add the `linkcheck` builder, add the following to your conf.py:

```python
sphinx_tabs_valid_builders = ['linkcheck']
```

If you are using [Read The Docs](https://readthedocs.org/) for building your documentation, the extension must be added as a requirement. Please add the following to `requirements.txt` at the root of the project:

```
sphinx-tabs==1.1.13
```

## Contributing

We welcome all contributions!
See the [EBP Contributing Guide](https://executablebooks.org/en/latest/contributing.html) for general details.

The simplest way to run tests is to install [pre-commit](https://pre-commit.com/) for linting and [tox](https://tox.readthedocs.io) for unit tests and documentation build:

```console
$ pre-commit run --all
```

```console
$ tox -p
```

## Basic Tabs

Basic tabs can be coded as follows:

```rst
.. tabs::

   .. tab:: Apples

      Apples are green, or sometimes red.

   .. tab:: Pears

      Pears are green.

   .. tab:: Oranges

      Oranges are orange.
```

![Tabs](/images/tabs.gif)

## Grouped Tabs

Tabs can be grouped, so that changing the current tab in one area changes the current tab in the
another area. For example:

```rst
.. tabs::

   .. group-tab:: Linux

      Linux Line 1

   .. group-tab:: Mac OSX

      Mac OSX Line 1

   .. group-tab:: Windows

      Windows Line 1

.. tabs::

   .. group-tab:: Linux

      Linux Line 1

   .. group-tab:: Mac OSX

      Mac OSX Line 1

   .. group-tab:: Windows

      Windows Line 1
```

![Group Tabs](/images/groupTabs.gif)

## Code Tabs

Tabs containing code areas with syntax highlighting can be created as follows:

```rst
.. tabs::

   .. code-tab:: c

         int main(const int argc, const char **argv) {
           return 0;
         }

   .. code-tab:: c++

         int main(const int argc, const char **argv) {
           return 0;
         }

   .. code-tab:: py

         def main():
             return

   .. code-tab:: java

         class Main {
             public static void main(String[] args) {
             }
         }

   .. code-tab:: julia

         function main()
         end

   .. code-tab:: fortran

         PROGRAM main
         END PROGRAM main
```

![Code Tabs](/images/codeTabs.gif)

[github-ci]: https://github.com/executablebooks/sphinx-tabs/workflows/continuous-integration/badge.svg?branch=master
[github-link]: https://github.com/executablebooks/sphinx-tabs
[pypi-badge]: https://img.shields.io/pypi/v/sphinx-tabs.svg
[pypi-link]: https://pypi.org/project/sphinx-tabs
[codecov-badge]: https://codecov.io/gh/executablebooks/sphinx-tabs/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/sphinx-tabs
