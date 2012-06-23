#!/bin/bash

START=`date '+%s'`
cd ../project
django-admin.py makemessages -a

cd ../apps
for fp in `find ../apps -mindepth 1 -maxdepth 1`; do
    cd $fp
    django-admin.py makemessages -a
done;

cd ../..
for fp in `find -name '*.po'`; do
    poedit $fp
done
