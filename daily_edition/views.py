import os
import threading

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core import management
from django.http import HttpResponseNotFound
from django.conf import settings
from publish_edition import get_settings_options

publish_settings = get_settings_options(settings)

@login_required
def edition(req, issue=None):
    if issue is None:
        basename = 'daily-edition.json'
    else:
        basename = 'issue-%s.json' % issue
    filename = os.path.join(publish_settings['output_dir'],
                            basename)
    if os.path.exists(filename):
        return render_to_response(
            'daily_edition/index.html',
            dict(issue_data=open(filename).read()),
            context_instance=RequestContext(req)
            )
    else:
        return HttpResponseNotFound()

def backup_file(filename):
    def mkfilename(i):
        return '%s.backup.%d' % (filename, i)

    i = 1
    backup_filename = mkfilename(i)
    while os.path.exists(backup_filename):
        i += 1
        backup_filename = mkfilename(i)

    contents = open(filename).read()
    open(backup_filename, 'w').write(contents)

@login_required
def edit_list(req):
    filename = publish_settings['authors_filename']
    if req.method == 'POST':
        backup_file(filename)
        open(filename, 'w').write(req.POST['text'])
        response = 'List saved.'
    else:
        response = ''
    text = open(filename).read()
    return render_to_response('daily_edition/edit_list.html', 
                              dict(text=text, response=response),
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
