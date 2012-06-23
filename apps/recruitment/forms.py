from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from recruitment.models import Person
import string

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user')

    def clean_ssn(self):
        ssn = ''.join(d for d in self.cleaned_data['ssn'] if d in string.digits)
        if not len(ssn) in (10, 12):
            raise forms.ValidationError(_(u'Social security number must have a length of 10 or 12 digits.'))

        return ssn

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
