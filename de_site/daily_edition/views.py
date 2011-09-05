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
from models import Person
import publish_edition as pedition
import multiuser

DEFAULT_AUTHORS = 'Christopher Blizzard\nMike Shaver\n'

def get_account(req):
    default_authors = getattr(settings, 'DAILY_EDITION_DEFAULT_LIST',
                              DEFAULT_AUTHORS)
    return multiuser.Account(root_dir=settings.DAILY_EDITION_ROOT_DIR,
                             default_authors=default_authors,
                             user=req.user)
    
@login_required
def edition(req, issue=None):
    acct = get_account(req)
    if acct.has_issue(issue):
        return render_to_response(
            'daily_edition/issue.html',
            dict(issue_data=acct.get_issue_json(issue)),
            context_instance=RequestContext(req)
            )
    else:
        return HttpResponseNotFound()

@login_required
def view_list(req):
    acct = get_account(req)
    people = pedition.get_people_info(Person, acct.authors_filename)
    return render_to_response('daily_edition/view_list.html',
                              dict(people=people),
                              context_instance=RequestContext(req))

@login_required
def edit_list(req):
    acct = get_account(req)
    if req.method == 'POST':
        acct.set_authors(req.POST['text'])
        messages.add_message(req, messages.INFO, 'List saved.')
        return redirect('view-list')
    text = open(acct.authors_filename).read()
    return render_to_response('daily_edition/edit_list.html', 
                              dict(text=text),
                              context_instance=RequestContext(req))

@login_required
def publish_edition(req):
    acct = get_account(req)
    if req.method == 'POST':
        options = dict(people=Person, update_urls=False)

        def publish():
            acct.publish_edition(pedition.publish_edition, **options)

        if 'refresh-feeds' in req.POST:
            options.update(dict(update_urls=True))
            t = threading.Thread(target=publish)
            t.start()
            messages.add_message(
                req,
                messages.INFO,
                ('Starting the presses. This may take a while, '
                 'since feeds are being refreshed. Keep reloading '
                 'the page until you see your new issue listed.')
                )
        else:
            publish()
            messages.add_message(req, messages.INFO, 'Issue published!')

        return HttpResponseRedirect(req.get_full_path())

    issues = acct.get_issue_history()[-5:]
    return render_to_response('daily_edition/publish_edition.html',
                              dict(issues=issues),
                              context_instance=RequestContext(req))
