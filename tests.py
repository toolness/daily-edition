"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os

from django.test import TestCase
from daily_edition.models import Person, Alias, Site
from daily_edition.management.commands import whoisi_import

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

def install_sample_data():
    cmd = whoisi_import.Command()
    cmd.handle(path('sample_data', 'people.json'), verbosity='0')

class SimpleTest(TestCase):
    def test_sites_relate_backward_to_person(self):
        install_sample_data()
        p = Person.objects.get(name='Christopher Blizzard')
        self.assertEqual(len(p.sites.all()), 10)
