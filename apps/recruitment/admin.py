from django.contrib import admin
from recruitment.models import Application, DriverLicense, ForkLiftLicense, Language, Person, Position, ShirtSize, StringTranslation, TextTranslation, StudyArea

admin.site.register(Application)
admin.site.register(DriverLicense)
admin.site.register(ForkLiftLicense)
admin.site.register(Language)
admin.site.register(Person)
admin.site.register(Position)
admin.site.register(ShirtSize)
admin.site.register(StudyArea)
admin.site.register(StringTranslation)
admin.site.register(TextTranslation)

