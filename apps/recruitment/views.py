from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils.translation import get_language, ugettext as _
from recruitment.forms import PersonForm, UserForm
from recruitment.models import DriverLicense, ForkLiftLicense, Language, Person, ShirtSize, StudyArea
import operator

def register(request):
    pform = PersonForm(request.POST or None, prefix='pf')

    # Pick only the alternatives with the right language
    for (field, model) in (('study_area', StudyArea), ('driver_license', DriverLicense), ('forklift_license', ForkLiftLicense), ('shirt_size', ShirtSize)):
       pform.fields[field].queryset = model.objects.filter(language__code__icontains=get_language())

    uform = UserForm(request.POST or None, prefix='uf')
    if request.method == 'POST':
        if all([f.is_valid() for f in (pform, uform)]):
            person = pform.save()

            password = User.objects.make_random_password(length=15)
            user = User.objects.create_user(uform.cleaned_data['username'], person.email, password)
            user.save()

            person.user = user
            person.save()

            # TODO: Add support for templates in database. 

            # Prepare an e-mail
            current_site  = Site.objects.get_current()
            mail_template = loader.get_template('recruitment/register_confirmation_mail.txt')
            mail_context  = RequestContext(request, {'person' : person, 'password' : password})

            # Send the mail to the user
            send_mail(_(u'[CHARM] Thank you for registering!'), mail_template.render(mail_context), 'noreply@%s' % current_site.domain, [person.email], fail_silently=True)

            # Set the person id in a session before redirection.
            # So we can retrieve the person on the confirmation page.
            request.session['pid'] = person.pk

            return HttpResponseRedirect(reverse('confirmation'))

    return render(request, 'recruitment/register.html', { 'page_title' : _(u'Register!'), 'button_text' : _(u'Register me!'), 'forms' : (pform, uform) })

def confirmation(request):
    # TODO: This doesn't feel secure enough. Maybe login is better? Or remove the session variable ASAP?
    person = Person.objects.get(pk=request.session['pid'])
    return render(request, 'recruitment/confirmation.html', { 'page_title' : _(u'Confirmation!'), 'person' : person })

@login_required
def mypage(request):
    return render(request, 'recruitment/mypage.html', {'page_title' : _(u'My page')})
    
def set_language(request, code):
    u"""Set the language session variable to code."""
    try:
        request.session['django_language'] = code
    except Language.DoesNotExist:
        pass
   
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
