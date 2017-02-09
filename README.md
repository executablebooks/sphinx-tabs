sphinx-tabs [![Build Status](https://travis-ci.org/djungelorm/sphinx-tabs.svg?branch=master)](https://travis-ci.org/djungelorm/sphinx-tabs)
========================================

Create tabbed content when building HTML

Check the [Raw] code of [test/index.rst](test/index.rst) to see the rst that generated these GIFs.

![Tabs](/images/tabs.gif)

Installation
----------------------------------------

```bash
pip install sphinx_tabs
```

To enable the extension in Sphinx, add the following to your conf.py:

```python
extensions = ['sphinx_tabs.tabs']
```

Tabs
----------------------------------------

![Tabs](/images/tabs.gif)

```rst
.. tabs::

   .. tab:: Apples

      Apples are green, or sometimes red.

   .. tab:: Pears

      Pears are green.

   .. tab:: Oranges

      Oranges are orange.
```

Group Tabs
----------------------------------------

![Group Tabs](/images/groupTabs.gif)

```rst
.. tabs::

   .. group-tab:: Linux

      Linux Line 1

   .. group-tab:: Mac OSX

      Mac OSX Line 1

   .. group-tab:: Windows

      Windows Line 1
```

Code Tabs
----------------------------------------

![Code Tabs](/images/codeTabs.gif)

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
