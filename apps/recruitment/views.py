from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from recruitment.forms import PersonForm, UserForm

def register(request):
    pform = PersonForm(request.POST or None, prefix='pf')
    uform = UserForm(request.POST or None, prefix='uf')
    if request.method == 'POST':
        if all([f.is_valid() for f in (pform, uform)]):
            person = pform.save()

            user = User.objects.create_user(uform.username, pform.email, User.objects.make_random_password(length=15))
            user.save()

            person.user = user
            person.save()

            # TODO: Send an e-mail.
            return HttpResponseRedirect(reverse('confirmation'))

    return render(request, 'recruitment/register.html', { 'page_title' : _(u'Register!'), 'button_text' : _(u'Register me!'), 'forms' : (pform, uform) })

def confirmation(request):
    return render(request, 'recruitment/confirmation.html', { 'page_title' : _(u'Confirmation!'), })
    
