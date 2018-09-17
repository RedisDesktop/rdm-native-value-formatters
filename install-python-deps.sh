#!/usr/bin/env bash
dirname "$0"
for i in ./*python*/; do
    cd $i
    if [ -f requirements.txt ]; then
        pip3 install -r requirements.txt
    fi
    cd ..
done

export PYTHONPATH=`pwd`