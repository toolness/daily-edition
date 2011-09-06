from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from daily_edition.models import Person
from daily_edition.multiuser import Account
import daily_edition.publish_edition as pedition

class Command(BaseCommand):
    help = 'Retrieves and caches all feeds for all users.'
    
    def handle(self, *args, **options):
        for user in User.objects.all():
            a = Account(root_dir=settings.DAILY_EDITION_ROOT_DIR,
                        user=user)
            if options['verbosity'] != '0':
                print "fetching all feeds for user %s" % user.username
            a.publish_edition(pedition.publish_edition,
                              people=Person,
                              update_only=True)
