from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from recruitment.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
