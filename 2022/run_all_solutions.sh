#!/bin/bash
export PYTHONIOENCODING=utf-8

rm -f solutions.txt

for day in {1..25}
do
    cd "dec$day"
    py ./solution.py --no-color | tee -a ../solutions.txt
    cd ..
done

read
