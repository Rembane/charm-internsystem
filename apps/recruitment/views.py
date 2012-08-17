# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from recruitment.forms import ApplicationForm, ApplicationCommentForm, PersonForm
from recruitment.models import Application, DriverLicense, ForkLiftLicense, Language, Person, ShirtSize, StudyArea
import operator

def register(request):
    pform = PersonForm(request.POST or None)

    # Remove the stupid help text.
    stupid_help_text = _(u'Hold down "Control", or "Command" on a Mac, to select more than one.')
    for field in ('driver_license', 'forklift_license'):
        pform.fields[field].help_text = pform.fields[field].help_text.replace(stupid_help_text, '').strip()

    if request.method == 'POST':
        if pform.is_valid():
            person = pform.save()

            password = User.objects.make_random_password(length=15)
            user = User.objects.create_user(person.email, person.email, password)
            user.save()

            person.user = user
            person.save()

            # TODO: Add support for templates in database. 

            # Prepare an e-mail
            current_site  = Site.objects.get_current()
            mail_template = loader.get_template('recruitment/register_confirmation_mail.txt')
            mail_context  = RequestContext(request, {'person' : person, 'password' : password, 'email_hash' : person.email_hash, 'domain' : current_site.domain})

            # Send the mail to the user
            send_mail(_(u'[CHARM] Thank you for registering!'), mail_template.render(mail_context), 'noreply@%s' % current_site.domain, [person.email], fail_silently=True)

            loggedin_user = authenticate(username=person.email, password=password)
            if loggedin_user is not None:
                messages.success(request, _(u'Thank you for registering. You will receive an e-mail within 24 hours with more information.'))
                login(request, loggedin_user)

            return HttpResponseRedirect(reverse('mypage'))

    return render(request, 'recruitment/register.html', { 'page_title' : _(u'Register!'), 'button_text' : _(u'Register!'), 'form' : pform })

@login_required
def mypage(request):
    return render(request, 'recruitment/mypage.html', {'page_title' : _(u'My page'), 'person' : Person.objects.get(user=request.user)})

def confirm_email_address(request, pk, email_hash):
    u"""Confirms the email adress if pk and email_hash are correct."""
    # TODO: UX-stuff, like giving the user a message about what happened and how.
    person = Person.objects.get(pk=pk)
    if person.email_hash == email_hash:
        person.email_confirmed = True
        person.save()

    return HttpResponseRedirect(reverse('mypage'))

@login_required
def edit_my_profile(request):
    u"""Edit the profile + the username of the user."""

    person = Person.objects.get(user=request.user)
    pform  = PersonForm(request.POST or None, instance=person)
    if request.method == 'POST':
        if pform.is_valid():
            personf = pform.save()

            request.user.username = personf.email
            request.user.email = personf.email
            request.user.save()

            return HttpResponseRedirect(reverse('mypage'))

    return render(request, 'recruitment/register.html', { 'page_title' : _(u'Edit my profile'), 'button_text' : _(u'Save!'), 'form' : pform })

@login_required
def apply_for_position(request):
    def join_preferred_positions(pfs):
        pfs = [p for p in pfs if p]
        pfslen = len(pfs)
        if pfslen == 1:
            return pfs[0]
        elif pfslen == 2:
            return _(u'and').join(unicode(pfs))
        else:
            return u'%s, %s %s %s' % (pfs[0], _(u'and'), pfs[1], pfs[2])

    # TODO: Make the process more user friendly.
    aform = ApplicationForm(request.POST or None)
    if request.method == 'POST':
        if aform.is_valid():
            application = aform.save(commit=False)
            application.person = Person.objects.get(user=request.user)
            application.save()

            messages.success(request, _(u'Thank you for applying to %s. You will within 24 hours receieve a confirmation mail with further instructions.') % join_preferred_positions((application.preferred_position1, application.preferred_position2, application.preferred_position3)))

            return HttpResponseRedirect(reverse('mypage') + u'#applications')

    return render(request, 'recruitment/register.html', { 'page_title' : _(u'Apply for position'), 'button_text' : _(u'Save!'), 'form' : aform })

def confirm_application(request, pk, confirmation_hash):
    u"""Confirms the email adress if pk and email_hash are correct."""
    # TODO: UX-stuff, like giving the user a message about what happened and how.
    application = Application.objects.get(pk=pk)
    if confirmation_hash == application.confirmation_hash:
        application.confirm()

    return HttpResponseRedirect(reverse('mypage'))

@permission_required('can_administrate')
def list_applications(request):
    return render(request, 'recruitment/list_applications.html', { 'page_title' : _(u'List applications'), 'applications' : Application.objects.all().order_by('-created').select_related()})
    
@permission_required('can_administrate')
def show_application(request, pk):
    application = Application.objects.get(pk=pk)
    if request.method == 'POST':
        mapping = {'pp1' : 'preferred_position1', 'pp2' : 'preferred_position2', 'pp3' : 'preferred_position3'}
        application.approve(getattr(application, filter(operator.truth, [mapping.get(k, None) for (k,v) in request.POST.iteritems()])[0]))

    return render(request, 'recruitment/show_application.html', { 'page_title' : _(u'Show application'), 'application' : application, 'acform' : ApplicationCommentForm(), 'button_text' : _(u'Comment!') })

@permission_required('can_administrate')
def add_application_comment(request, pk):
    u"""Saves a comment."""
    if request.method == 'POST':
        acform = ApplicationCommentForm(request.POST)
        if acform.is_valid():
            ac = acform.save(commit=False)
            ac.application = Application.objects.get(pk=pk)
            ac.person = Person.objects.get(user=request.user)
            ac.save()

    return HttpResponseRedirect(reverse('show_application', args=[pk]))


def set_language(request, code):
    u"""Set the language session variable to code."""
    try:
        request.session['django_language'] = code
    except Language.DoesNotExist:
        pass
   
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


