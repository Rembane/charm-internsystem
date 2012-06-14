from django.contrib import admin
from recruitment.models import DriverLicense, ForkLiftLicense, Language, Person, ShirtSize, StudyArea

admin.site.register(DriverLicense)
admin.site.register(ForkLiftLicense)
admin.site.register(Language)
admin.site.register(Person)
admin.site.register(ShirtSize)
admin.site.register(StudyArea)

