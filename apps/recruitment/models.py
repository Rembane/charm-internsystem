from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

class Language(models.Model):
    u"""http://www.i18nguy.com/unicode/language-identifiers.html"""
    code = models.CharField(ugettext_lazy(u'Language code'), max_length=50)
    name = models.CharField(ugettext_lazy(u'Language name'), max_length=50)

    class Meta:
        verbose_name = ugettext_lazy(u'language')
        verbose_name_plural = ugettext_lazy(u'languages')

    def __unicode__(self):
        return u'%s %s' % (self.code, self.name)

class StudyArea(models.Model):
    title = models.CharField(ugettext_lazy(u'Area of study'), max_length=50) # TODO: Better name!
    language = models.ForeignKey(Language)
    main = models.ForeignKey('self', blank=True, null=True, help_text=ugettext_lazy(u'Pointing to the main language.'))

    class Meta:
        verbose_name = ugettext_lazy(u'area of study')
        verbose_name_plural = ugettext_lazy(u'areas of study')

    def __unicode__(self):
        return self.title

class DriverLicense(models.Model):
    name = models.CharField(ugettext_lazy(u'Name'), max_length=25)
    language = models.ForeignKey(Language)
    main = models.ForeignKey('self', blank=True, null=True, help_text=ugettext_lazy(u'Pointing to the main language.'))

    class Meta:
        verbose_name = ugettext_lazy(u'driver license')
        verbose_name_plural = ugettext_lazy(u'driver licenses')

    def __unicode__(self):
        return self.name

class ForkLiftLicense(models.Model):
    name = models.CharField(ugettext_lazy(u'Name'), max_length=25)
    language = models.ForeignKey(Language)
    main = models.ForeignKey('self', blank=True, null=True, help_text=ugettext_lazy(u'Pointing to the main language.'))

    class Meta:
        verbose_name = ugettext_lazy(u'forklift license')
        verbose_name_plural = ugettext_lazy(u'forklift licenses')

    def __unicode__(self):
        return self.name

class ShirtSize(models.Model):
    name = models.CharField(ugettext_lazy(u'Name'), max_length=25)
    language = models.ForeignKey(Language)
    main = models.ForeignKey('self', blank=True, null=True, help_text=ugettext_lazy(u'Pointing to the main language.'))

    class Meta:
        verbose_name = ugettext_lazy(u'shirt size')
        verbose_name_plural = ugettext_lazy(u'shirt sizes')

    def __unicode__(self):
        return self.name

class Person(models.Model):
    u"""Contains information about a person."""
    fname = models.CharField(ugettext_lazy(u'First name'), max_length=50)
    lname = models.CharField(ugettext_lazy(u'Last name'), max_length=50)
    ssn = models.CharField(ugettext_lazy(u'Social security number'), help_text=ugettext_lazy(u'Enter your social security number, using ten or twelve digits.'), max_length=50)
    phone = models.CharField(ugettext_lazy(u'Phone number'), max_length=15) # Phone numbers are max 15 digits long.
    email = models.EmailField(ugettext_lazy(u'E-mail'), max_length=50)

    study_area = models.ForeignKey(StudyArea, verbose_name=ugettext_lazy(u'area of study')) # , verbose_name=ugettext_lazy(), verbose_name_plural=ugettext_lazy()
    starting_year = models.IntegerField(ugettext_lazy(u'Starting year'))
    driver_license = models.ManyToManyField(DriverLicense, verbose_name=ugettext_lazy(u'driver license')) 
    forklift_license = models.ManyToManyField(ForkLiftLicense, verbose_name=ugettext_lazy(u'forklift license'), help_text=ugettext_lazy(u'<a href="http://en.wikipedia.org/wiki/Forklift_Driver_Klaus_-_The_First_Day_on_the_Job">Safety first!</a>')) 
    allergies = models.TextField(ugettext_lazy(u'Allergies and food preferences'))
    shirt_size = models.ForeignKey(ShirtSize, verbose_name=ugettext_lazy(u'shirt size'))

    user = models.ForeignKey(User, blank=True, null=True)

    created = models.DateTimeField(ugettext_lazy(u'Created'), auto_now_add=True) 

    class Meta:
        verbose_name = ugettext_lazy(u'person')
        verbose_name_plural = ugettext_lazy(u'people')
        ordering = ('fname', 'lname')

    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)
    
