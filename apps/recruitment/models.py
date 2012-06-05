from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

class StudyArea(models.Model):
    title = models.CharField(_(u'Area of study'), max_length=50) # TODO: Better name!

class DriverLicense(models.Model):
    name = models.CharField(_(u'Name'), max_length=25)

class ForkLiftLicense(models.Model):
    name = models.CharField(_(u'Name'), max_length=25)

class ShirtSize(models.Model):
    name = models.CharField(_(u'Name'), max_length=25)

class Person(models.Model):
    u"""Contains information about a person."""
    class Meta:
        verbose_name = ugettext_lazy(u'Person')
        verbose_name_plural = ugettext_lazy(u'People')
        ordering = ('fname', 'lname')

#    DRIVERS_LICENSE_CHOICES = (
#        ('A', _(u'Motorcycle')),
#        ('B', _(u'Car')),
#        ('BE', _(u'Car with trailer')),
#        ('C', _(u'Truck')),
#        ('CE', _(u'Truck with trailer')),
#        ('D', _(u'Bus')),
#        ('DE', _(u'Bus with trailer')),
#    )
#
#    FORKLIFT_LICENSE_CHOICES = (
#        ('A2', _(u'A2')),
#        ('A3', _(u'A3')),
#        ('A4', _(u'A4')),
#        ('B1', _(u'B1')),
#        ('B2', _(u'B2')),
#        ('B3', _(u'B3')),
#        ('B6', _(u'B6')),
#        ('C1', _(u'C1')),
#        ('C2', _(u'C2')),
#        ('C5', _(u'C5')),
#    )
#    SHIRT_SIZE_CHOICES =  ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']

    fname = models.CharField(_(u'First name'), max_length=50)
    lname = models.CharField(_(u'Last name'), max_length=50)
    ssn = models.CharField(_(u'Social security number'), help_text=ugettext_lazy(u'Enter your social security number, using ten or twelve digits.'), max_length=50)
    phone = models.CharField(_(u'Phone number'), max_length=15) # Phone numbers are max 15 digits long.
    email = models.EmailField(_(u'E-mail'), max_length=50)

    study_area = models.ForeignKey(StudyArea)
    starting_year = models.IntegerField(_(u'Starting year'))
    driver_license = models.ManyToManyField(DriverLicense) # _(u'Drivers license')
    forklift_license = models.ManyToManyField(ForkLiftLicense, help_text=ugettext_lazy(u'<a href="http://en.wikipedia.org/wiki/Forklift_Driver_Klaus_-_The_First_Day_on_the_Job">Safety first!</a>')) # _(u'Forklift license')
    allergies = models.TextField(_(u'Allergies and food preferences'))
    shirt_size = models.ForeignKey(ShirtSize)

    user = models.ForeignKey(User, blank=True, null=True)

    created = models.DateTimeField(_(u'Created'), auto_now_add=True) 

    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)
    
