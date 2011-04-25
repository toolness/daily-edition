"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os

from django.test import TestCase
from django.contrib.auth.models import User
from daily_edition.models import Person, Alias, Site, OrderedFollow
from daily_edition.management.commands import whoisi_import

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

def install_sample_data():
    cmd = whoisi_import.Command()
    cmd.handle(path('sample_data', 'whoisi_export.json'), verbosity='0')

def test_sites_short_title_works(self):
    """
    >>> install_sample_data()
    >>> p = Person.objects.get(name='Christopher Blizzard')
    >>> linkedin = p.sites.get(kind='linkedin')
    >>> print linkedin.title
    None
    >>> print linkedin.short_title
    LinkedIn
    >>> blog = p.sites.get(url='http://www.0xdeadbeef.com/weblog')
    >>> print blog.title
    Christopher Blizzard
    >>> print blog.short_title
    0xdeadbeef.com
    >>> bliptv = p.sites.get(url='http://chrisblizzard.blip.tv')
    >>> print bliptv.short_title
    chrisblizzard.blip.tv
    """
    
    pass

class SimpleTest(TestCase):
    def test_sites_relate_backward_to_person(self):
        install_sample_data()
        p = Person.objects.get(name='Christopher Blizzard')
        self.assertEqual(len(p.sites.all()), 10)

    def test_ordered_follow_works(self):
        install_sample_data()
        chris = Person.objects.get(name='Christopher Blizzard')
        john = User(username='john')
        chris.save()
        john.save()
        f = OrderedFollow(user=john, person=chris, priority=1)
        f.save()
        self.assertEqual(chris.followers.all()[0], john)
        self.assertEqual(john.influencers.all()[0], chris)

# Run more tests.

from test_publish_edition import *
from test_multiuser import *
