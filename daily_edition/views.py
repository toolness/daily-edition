import threading

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core import management

@login_required
def publish_edition(req):
    if req.method == 'POST':
        if 'refresh-feeds' in req.POST:
            options = dict(update_urls=True)
            response = ('Starting the presses. This may take a while, '
                        'since feeds are being refreshed.')
        else:
            options = {}
            response = 'Starting the presses.'
        
        def start_job():
            management.call_command('publish_edition', **options)

        t = threading.Thread(target=start_job)
        t.start()
    else:
        response = ''
    context = dict(response=response)
    context.update(csrf(req))
    return render_to_response('daily_edition/publish_edition.html',
                              context)
