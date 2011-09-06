import sys

import django.utils.simplejson as json
from django.core.management.base import BaseCommand, CommandError
from daily_edition.models import Person, Site, Alias

class Command(BaseCommand):
    args = '<json_file>'
    help = 'Imports the specified JSON export from whoisi'
    
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Need a whoisi JSON export file.')
        people = json.load(open(args[0]))
        if options['verbosity'] != '0':
            sys.stdout.write("Adding people...")
            sys.stdout.flush()
        for person in people:
            if options['verbosity'] != '0':
                sys.stdout.write(".")
                sys.stdout.flush()
            p = Person(name=person['name'])
            p.save()
            for alias in person['aliases']:
                a = Alias(name=alias, person=p)
                a.save()
            for site in person['sites'].values():
                s = Site(kind=site['type'],
                         url=site['url'],
                         feed=site['feed'],
                         title=site['title'],
                         person=p)
                s.save()
        if options['verbosity'] != '0':
            print
            print "Done."
