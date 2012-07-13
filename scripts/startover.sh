#!/bin/bash

rm -rf ../apps/recruitment/migrations
rm -f ../dev.db

python ../manage.py syncdb --noinput

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'test')" | ../manage.py shell

python ../manage.py convert_to_south recruitment

./import_recruitment_data.py
