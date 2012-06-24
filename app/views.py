from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from app.models import Entry, Member, BeadCount, BeadEntry
import datetime
import json
import string

# The main page. Shows all the blog entries (might change this to the last n entries later).
def main_page(request):
    entries = Entry.objects.order_by('-date')
    if datetime.date.today().year == 2012:
        date = '2012'
    else:
        date = '2012 -- %s' % datetime.date.today().year
    return render_to_response('blog.html',
                              {'entries': entries,
                               'date': date},
                              context_instance=RequestContext(request))

# Shows one entry, based on its normalized title.
def entry(request, title):
    info = {}
    try:
        entry = Entry.objects.get(normalized_title=title)
        info['entries'] = [entry]
    except:
        pass
    return render_to_response('blog.html',
                              info,
                              context_instance=RequestContext(request))

# If name is None, shows the whole team page. Otherwise, shows that person's page.
def team(request, name=None):
    if name:
        names = string.split(name, '-')
        member = Member.objects.get(first_name=names[0], last_name=names[1])
        return render_to_response('team_member.html',
                                  {'member': member},
                                  context_instance=RequestContext(request))
    else:
        members = Member.objects.all()
        return render_to_response('team.html',
                                  {'members': members},
                                  context_instance=RequestContext(request))

# Shows the current bead count and the list of bead posts.
def beads(request):
    count = BeadCount.objects.get(id=1).beadcount
    entries = BeadEntry.objects.all()
    return render_to_response('beads.html',
                              {'count': count,
                               'entries': entries},
                              context_instance=RequestContext(request))

# Show all our photos.
def photos(request):
    return HttpResponse('Foo!')

@csrf_exempt
def post(request):
    if request.method != 'POST':
        return HttpResponse('failure!')
    entry_data = json.load(request)
    passhash = entry_data['password']
    with open('./password') as passfile:
        word = passfile.read()
        passhash += '\n'
        if passhash != word:
            return HttpResponse('password failure!')
    title = entry_data['title']
    normalized_title = entry_data['normalized_title']
    tagline = entry_data['tagline']
    body = entry_data['body']
    date = datetime.datetime.today()
    entry = Entry(title=title, normalized_title=normalized_title,
                  tagline=tagline, body=body, date=date)
    entry.save()
    return HttpResponse('success!')
