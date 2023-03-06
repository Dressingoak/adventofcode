#!/bin/bash
export PYTHONIOENCODING=utf-8

rm -f solutions.txt

for day in {1..25}
do
    py . --no-color "dec$day" | tee -a solutions.txt
done

read
