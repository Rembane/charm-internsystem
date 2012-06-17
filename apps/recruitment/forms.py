from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from recruitment.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user')

class UserForm(forms.Form):
    username = forms.CharField(label=ugettext_lazy(u'Username'), help_text=ugettext_lazy(u'Please enter your prefered username.'))
