#!/usr/bin/env bash

for i in ./*python*/; do
    cd $i
    if [ -f requirements.txt ]; then
        pip3 install -r requirements.txt
    fi
    cd ..
done