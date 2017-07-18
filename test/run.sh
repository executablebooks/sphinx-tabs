#!/bin/bash

set -ev

sphinx-build -E -n -W test/basic test-output-basic
sphinx-build -E -n -W test/notabs test-output-notabs
sphinx-build -E -n -W test/conditionalassets test-output-conditionalassets
