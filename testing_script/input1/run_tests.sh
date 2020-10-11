#!/bin/sh
> output.txt
for f in *.py
do
    printf "\nPYTHON SCRIPT $f:\n" >> output.txt
    for i in 1 2 3 4 5
    do
        printf "\nRUN $i:\n" >> output.txt
        python3 $(dirname $0)/$f >> output.txt
    done
done