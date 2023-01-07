#!/bin/bash
export PYTHONIOENCODING=utf-8

for day in {1..25}
do
    cd "dec$day"
    py -m unittest
    cd ..
done

read
