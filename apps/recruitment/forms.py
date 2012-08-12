# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import CheckboxSelectMultiple 
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from recruitment.models import Application, Person
import string

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('person', 'state')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user', 'email_confirmed')

        widgets = {
                'driver_license' : CheckboxSelectMultiple(),
                'forklift_license' : CheckboxSelectMultiple()
                }

    def clean_ssn(self):
        ssn = ''.join(d for d in self.cleaned_data['ssn'] if d in string.digits)
        if not len(ssn) in (10, 12):
            raise forms.ValidationError(_(u'Social security number must have a length of 10 or 12 digits.'))

        return ssn
