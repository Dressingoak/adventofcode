#!/bin/bash
export PYTHONIOENCODING=utf-8

rm -f solutions.txt

for day in {1..25}
do
    py . "dec$day" --no-color | tee -a solutions.txt
done

read
