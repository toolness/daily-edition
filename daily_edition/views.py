import os
import threading

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core import management
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from publish_edition import get_settings_options, get_matching_people, \
                            backup_file
from models import Person

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
            'daily_edition/issue.html',
            dict(issue_data=open(filename).read()),
            context_instance=RequestContext(req)
            )
    else:
        return HttpResponseNotFound()

@login_required
def view_list(req):
    filename = publish_settings['authors_filename']
    matches, names, unknown_names = get_matching_people(Person, filename)
    people = []
    for name in names:
        if name in unknown_names:
            people.append(dict(name=name, tags='unknown', is_unknown=True))
        else:
            people.append(dict(name=name, tags='known', is_unknown=False,
                               info=Person.objects.get(name=name)))
    return render_to_response('daily_edition/view_list.html',
                              dict(people=people),
                              context_instance=RequestContext(req))

@login_required
def edit_list(req):
    filename = publish_settings['authors_filename']
    if req.method == 'POST':
        backup_file(filename)
        open(filename, 'w').write(req.POST['text'])
        messages.add_message(req, messages.INFO, 'List saved.')
        return redirect('view-list')
    text = open(filename).read()
    return render_to_response('daily_edition/edit_list.html', 
                              dict(text=text),
                              context_instance=RequestContext(req))

@login_required
def publish_edition(req):
    if req.method == 'POST':
        if 'refresh-feeds' in req.POST:
            options = dict(update_urls=True)
            messages.add_message(
                req,
                messages.INFO,
                ('Starting the presses. This may take a while, '
                 'since feeds are being refreshed.')
                )
        else:
            options = {}
            messages.add_message(req, messages.INFO, 'Starting the presses.')
        
        def start_job():
            management.call_command('publish_edition', **options)

        t = threading.Thread(target=start_job)
        t.start()
        return HttpResponseRedirect(req.get_full_path())

    return render_to_response('daily_edition/publish_edition.html',
                              {},
                              context_instance=RequestContext(req))
