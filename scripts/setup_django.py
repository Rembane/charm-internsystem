# -*- coding: utf-8 -*-

import os.path, sys

try:
    from django.core.management import setup_environ
except ImportError:
    for row in sys.path:
        print row
    raise
from project import settings

setup_environ(settings)

