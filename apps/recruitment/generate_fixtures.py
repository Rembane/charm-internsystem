#!/usr/bin/env python

u"""This script prints fixtures from some default data to stdout. 

It's insanely ugly but does what it should."""

import json

template = u"""    {
        "fields": %s,
        "model": "recruitment.%s", 
        "pk": %s
    }, 
"""

# Generate forklift licenses
pk = 1
for f in ('A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B6', 'C1', 'C2', 'C5'):
    fields = lambda name, language, main: {
            'name' : name, 
            'language' : language,
            'main' : main}

    print template % (json.dumps(fields(f, 2, None)), 'forkliftlicense', pk)
    pk += 1
    print template % (json.dumps(fields(f, 1, pk-1)), 'forkliftlicense', pk)
    pk += 1

# Generate t-shirt sizes
pk = 1
for s in ('XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'):
    fields = lambda name, language, main: {
            'name' : name, 
            'language' : language,
            'main' : main}

    print template % (json.dumps(fields(s, 2, None)), 'shirtsize', pk)
    pk += 1
    print template % (json.dumps(fields(s, 1, pk-1)), 'shirtsize', pk)
    pk += 1

