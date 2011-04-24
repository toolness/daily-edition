import os
import threading

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core import management
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from publish_edition import get_settings_options

publish_settings = get_settings_options(settings)

def output_json_or_404(basename):
    filename = os.path.join(publish_settings['output_dir'],
                            basename)
    if os.path.exists(filename):
        return HttpResponse(open(filename).read(),
                            mimetype='application/json')
    else:
        return HttpResponseNotFound()

@login_required
def latest_edition_json(req):
    return output_json_or_404('daily-edition.json')
    
@login_required
def edition_json(req, issue):
    return output_json_or_404('issue-%s.json' % issue)

@login_required
def edition(req, issue=None):
    return render_to_response('daily_edition/index.html', {},
                              context_instance=RequestContext(req))

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
    return render_to_response('daily_edition/publish_edition.html',
                              {'response': response},
                              context_instance=RequestContext(req))
