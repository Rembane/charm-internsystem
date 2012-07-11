#!/usr/bin/env python

u"""This script imports some useful data."""

from setup_django import *
from recruitment.models import DriverLicense, ForkLiftLicense, Language, ShirtSize, StringTranslation, StudyArea
import itertools

# Generate languages
ls = [(Language.objects.get_or_create(code=code, name=name)[0], default) for (code, name, default) in (('en', 'English', True), ('sv', 'Swedish', False))]

data = (
    # Generate forklift licenses
    (ForkLiftLicense, ('A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B6', 'C1', 'C2', 'C5')),

    # Generate t-shirt sizes
    (ShirtSize, ('XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL')),

    (StudyArea, (('Computer engineering', 'Datateknik'), ('Construction engineering', 'Byggteknik'))),

    (DriverLicense, ((u'A Motorcycle', u'A Motorcykel'), (u'B Car', u'B Bil'), (u'BE Car with trailer', u'BE Bil med tungt sl\xe4p'), (u'C Truck', u'C Lastbil'), (u'CE Truck with trailer', u'CE Lastbil med sl\xe4p'), (u'D Bus', u'D Buss'), (u'DE Bus with trailer', u'DE Buss med sl\xe4p'))),

)

for model, ss in data:
    for s in ss:
        o = model.objects.create()
        if type(s) == type(tuple()):
            o.translations = [StringTranslation.objects.create(string=x, language=lang, default=default) for ((lang, default),x) in zip(ls, itertools.cycle(s))]
        else:
            o.translations = [StringTranslation.objects.create(string=s, language=lang, default=default) for (lang, default) in ls]

        


