#!/bin/bash

set -ev

testnames=(basic notabs conditionalassets nestedmarkup)
builders=(html singlehtml dirhtml)

mkdir -p test-output
for builder in "${builders[@]}"
do
    for testname in "${testnames[@]}"
    do
        sphinx-build -b $builder -E -n -W test/$testname test-output/$builder-$testname
    done
done
