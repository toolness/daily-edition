from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from daily_edition.old.publish_edition import parser_options, \
                                              publish_edition, \
                                              set_stdout
from daily_edition.models import Person, Site, Alias

class Command(BaseCommand):
    args = '<json_file>'
    help = 'Publishes a Daily Edition.'
    option_list = list(BaseCommand.option_list)
    
    for args, kwargs in parser_options.items():
        option_list.append(make_option(*args, **kwargs))
    del args
    del kwargs

    def handle(self, *args, **options):
        kwargnames = [o['dest'] for o in parser_options.values()]
        kwargs = {}
        for name in kwargnames:
            kwargs[name] = options[name]

        # Unfortunately, options come to us pre-defaulted, which is
        # a bit annoying since there's no easy way to tell if they
        # were specified on the command line so we can have 
        # command-line options override ones defined in settings.
        #
        # So, for now we just have to have settings override the
        # command-line options.

        if getattr(settings, 'DAILY_EDITION', None):
            de_settings = settings.DAILY_EDITION
            for name in kwargnames:
                if name in de_settings:
                    kwargs[name] = de_settings[name]
        set_stdout(self.stdout)
        publish_edition(Person, **kwargs)
