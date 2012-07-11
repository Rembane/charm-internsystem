# -*- coding: utf-8 -*-

from django_fsm.db.fields import FSMField, transition
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import get_language, ugettext_lazy, ugettext as _

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

    class Meta:
        verbose_name = ugettext_lazy(u'person')
        verbose_name_plural = ugettext_lazy(u'people')
        ordering = ('fname', 'lname')

        permissions = (
                    (u'can_administrate', _(u'Can administrate')),
                )

    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)
    
class Application(models.Model):
    person = models.ForeignKey(Person)
    state = FSMField(ugettext_lazy(u'State'), default=ugettext_lazy(u'applied'), protected=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ugettext_lazy(u'application')
        verbose_name_plural = ugettext_lazy(u'applications')

    @transition(source=u'applied', target=u'approved', save=True)
    def approve(self):
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

