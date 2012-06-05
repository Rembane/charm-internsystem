from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from recruitment.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user')

class UserForm(forms.Form):
    username = forms.CharField(label=_(u'Username'), help_text=ugettext_lazy(u'Please type in the username you wish to login with.'))
