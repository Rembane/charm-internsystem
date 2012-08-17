# -*- coding: utf-8 -*-

from django_fsm.db.fields import FSMField, transition
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.template import Context, loader
from django.utils.translation import get_language, ugettext_lazy, ugettext as _
import hashlib

class Language(models.Model):
    u"""http://www.i18nguy.com/unicode/language-identifiers.html"""
    code = models.CharField(ugettext_lazy(u'Language code'), max_length=50)
    name = models.CharField(ugettext_lazy(u'Language name'), max_length=50)

    class Meta:
        verbose_name = ugettext_lazy(u'language')
        verbose_name_plural = ugettext_lazy(u'languages')

    def __unicode__(self):
        return u'%s %s' % (self.code, self.name)

class StringTranslation(models.Model):
    u"""A translation for a string."""
    string   = models.CharField(ugettext_lazy(u'String'), max_length=25)
    language = models.ForeignKey(Language)
    default  = models.BooleanField(ugettext_lazy(u'Default language'), default=False)

    class Meta:
        verbose_name = ugettext_lazy(u'string translation')
        verbose_name_plural = ugettext_lazy(u'string translations')

    def __unicode__(self):
        return self.string

class TextTranslation(models.Model):
    u"""A translation for a text."""
    text     = models.TextField(ugettext_lazy(u'Text'))
    language = models.ForeignKey(Language)
    default  = models.BooleanField(ugettext_lazy(u'Default language'), default=False)

    class Meta:
        verbose_name = ugettext_lazy(u'text translation')
        verbose_name_plural = ugettext_lazy(u'text translations')

    def __unicode__(self):
        return self.text

class BaseInfo(models.Model):
    translations = models.ManyToManyField(StringTranslation)

    class Meta:
        abstract = True
        ordering = ('translations__string',)

    def __unicode__(self):
        u"""Either get the language we want, or get the default language. 
        Will probably throw terrible exceptions if neither is found. 
        That's a feature. The translations are regarded as broken if 
        neither a translation nor a default exists."""
        lang = get_language().lower()
        ts   = self.translations.filter(Q(language__code__icontains=lang) | Q(default=True)).select_related(depth=2)
        if len(ts) > 1:
            for t in ts:
                if lang in t.language.code.lower():
                    return t.string
        else:
            if ts[0].default:
                return ts[0].string

        assert False, u'Got neither a translation nor a default language for %s, id: %s' % (self, self.pk)

class StudyArea(BaseInfo):
    class Meta:
        verbose_name = ugettext_lazy(u'area of study')
        verbose_name_plural = ugettext_lazy(u'areas of study')

class DriverLicense(BaseInfo):
    class Meta:
        verbose_name = ugettext_lazy(u'driver license')
        verbose_name_plural = ugettext_lazy(u'driver licenses')

class ForkLiftLicense(BaseInfo):
    class Meta:
        verbose_name = ugettext_lazy(u'forklift license')
        verbose_name_plural = ugettext_lazy(u'forklift licenses')

class ShirtSize(BaseInfo):
    class Meta:
        verbose_name = ugettext_lazy(u'shirt size')
        verbose_name_plural = ugettext_lazy(u'shirt sizes')

class Person(models.Model):
    u"""Contains information about a person."""
    fname = models.CharField(ugettext_lazy(u'First name'), max_length=50)
    lname = models.CharField(ugettext_lazy(u'Last name'), max_length=50)
    ssn = models.CharField(ugettext_lazy(u'Social security number'), help_text=ugettext_lazy(u'Enter your social security number, using ten or twelve digits.'), max_length=50)
    phone = models.CharField(ugettext_lazy(u'Phone number'), max_length=15) # Phone numbers are max 15 digits long.
    email = models.EmailField(ugettext_lazy(u'E-mail'), max_length=50)

    study_area = models.ForeignKey(StudyArea, verbose_name=ugettext_lazy(u'area of study')) # , verbose_name=ugettext_lazy(), verbose_name_plural=ugettext_lazy()
    starting_year = models.IntegerField(ugettext_lazy(u'Starting year'))
    driver_license = models.ManyToManyField(DriverLicense, verbose_name=ugettext_lazy(u'driver license'), null=True, blank=True) 
    forklift_license = models.ManyToManyField(ForkLiftLicense, verbose_name=ugettext_lazy(u'forklift license'), help_text=ugettext_lazy(u'<a href="http://www.youtube.com/watch?v=9z77oztO6UQ">Safety first!</a>'), null=True, blank=True) 
    allergies = models.TextField(ugettext_lazy(u'Allergies and food preferences'), blank=True)
    shirt_size = models.ForeignKey(ShirtSize, verbose_name=ugettext_lazy(u'shirt size'))

    # TODO: Gör om till OneToOneField
    user = models.ForeignKey(User, blank=True, null=True)

    created = models.DateTimeField(ugettext_lazy(u'Created'), auto_now_add=True) 
    email_confirmed = models.BooleanField(ugettext_lazy(u'E-mail address confirmed'), default=False)

    class Meta:
        verbose_name = ugettext_lazy(u'person')
        verbose_name_plural = ugettext_lazy(u'people')
        ordering = ('fname', 'lname')

        permissions = (
                    (u'can_administrate', _(u'Can administrate')),
                )

    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)

    @property
    def email_hash(self):
        return hashlib.sha1(self.email).hexdigest()

class Position(models.Model):
    u"""A position within the CHARM organisation."""

    name_translations = models.ManyToManyField(StringTranslation)
    description_translations = models.ManyToManyField(TextTranslation)

    @property
    def name(self):
        u"""Either get the language we want, or get the default language. 
        Will probably throw terrible exceptions if neither is found. 
        That's a feature. The translations are regarded as broken if 
        neither a translation nor a default exists.
        
        This one breaks DRY, the original one is in BaseInfo."""
        lang = get_language().lower()
        ts   = self.name_translations.filter(Q(language__code__icontains=lang) | Q(default=True)).select_related(depth=2)
        if len(ts) > 1:
            for t in ts:
                if lang in t.language.code.lower():
                    return t.string
        else:
            if ts[0].default:
                return ts[0].string

        assert False, u'Got neither a translation nor a default language for %s, id: %s' % (self, self.pk)

    @property
    def description(self):
        u"""Either get the language we want, or get the default language. 
        Will probably throw terrible exceptions if neither is found. 
        That's a feature. The translations are regarded as broken if 
        neither a translation nor a default exists.
        
        This one breaks DRY, the original one is in BaseInfo."""
        lang = get_language().lower()
        ts   = self.description_translations.filter(Q(language__code__icontains=lang) | Q(default=True)).select_related(depth=2)
        if len(ts) > 1:
            for t in ts:
                if lang in t.language.code.lower():
                    return t.string
        else:
            if ts[0].default:
                return ts[0].string

        assert False, u'Got neither a translation nor a default language for %s, id: %s' % (self, self.pk)

    def __unicode__(self):
        return self.name

class Application(models.Model):
    person = models.ForeignKey(Person)
    state = FSMField(u'State', default=u'applied', protected=True, editable=False)

    suitability_motivation = models.CharField(ugettext_lazy(u'Are you suitable?'), help_text=ugettext_lazy(u'Motivate why you would do a good job at this post.'), max_length=255)
    preferred_position1 = models.ForeignKey(Position, verbose_name=ugettext_lazy(u'Your first preferred position'), related_name=u'application_set1')
    preferred_position2 = models.ForeignKey(Position, verbose_name=ugettext_lazy(u'Your second preferred position'), related_name=u'application_set2', blank=True, null=True) 
    preferred_position3 = models.ForeignKey(Position, verbose_name=ugettext_lazy(u'Your third preferred position'), related_name=u'application_set3', blank=True, null=True)
    approved_position = models.ForeignKey(Position, verbose_name=ugettext_lazy(u'Approved position'), related_name=u'approved_application_set', blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy(u'application')
        verbose_name_plural = ugettext_lazy(u'applications')

    @property
    def translated_state(self):
        # TODO: Put the translations dictionary somewhere else, where
        # we only need to translate it a few times, like a constructor
        # or something.
        translations = {
                u'applied' : _(u'applied'),
                u'approved' : _(u'approved'),
                u'approved_not_confirmed' : _(u'approved_not_confirmed'),
                u'not_approved' : _(u'not_approved'),
                u'reserve' : _(u'reserve'),
                u'dropped_out' : _(u'dropped_out'),
            }

        return translations[self.state]

    @property
    def confirmation_hash(self):
        return hashlib.sha1(unicode(self.person) + unicode(self.created)).hexdigest()

    def __unicode__(self):
        return u'%s, %s' % (self.person, self.translated_state)

    @transition(source=u'applied', target=u'approved_not_confirmed', save=True)
    def approve(self, position):
        self.approved_position = position
        
        # Prepare an e-mail
        current_site  = Site.objects.get_current()
        mail_template = loader.get_template('recruitment/apply_confirmation_mail.txt')
        mail_context  = Context({'position' : position, 'pk' : self.pk, 'confirmation_hash' : self.confirmation_hash, 'domain' : current_site.domain})

        # Send the mail to the user
        send_mail(_(u'[CHARM] You have been approved for %s!') % position, mail_template.render(mail_context), 'noreply@%s' % current_site.domain, [self.person.email], fail_silently=True)


    @transition(source=u'approved_not_confirmed', target=u'approved', save=True)
    def confirm(self):
        pass

    @transition(source=u'applied', target=u'not_approved', save=True)
    def not_approve(self):
        pass

    @transition(source=u'applied', target=u'reserve', save=True)
    def put_in_reserve(self):
        pass

    @transition(source=u'*', target=u'dropped_out', save=True)
    def drop_out(self):
        pass

    @transition(source=u'*', target=u'applied', save=True)
    def reset(self):
        self.approved_position = None


class ApplicationComment(models.Model):
    text = models.TextField(ugettext_lazy(u'Comment'))
    person = models.ForeignKey(Person, verbose_name=ugettext_lazy(u'Person'))
    application = models.ForeignKey(Application, verbose_name=ugettext_lazy(u'Application'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ugettext_lazy(u'application comment')
        verbose_name_plural = ugettext_lazy(u'application comments')
        ordering = ('created', )

    def __unicode__(self):
        return u'%s: %s' % (self.person, self.text)
