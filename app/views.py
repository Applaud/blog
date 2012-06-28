from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from app.models import Entry, Member, BeadCount, BeadEntry
import datetime
import json
import string
from blog import settings

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

def save_entry(request):
    print 'saving entry'
    entry_data = json.load(request)
    title = entry_data['title']
    if not pass_ok(entry_data['password']):
        return HttpResponse('password failure!')
    print 'password OK'
    normalized_title = entry_data['normalized_title']
    tagline = entry_data['tagline']
    body = entry_data['body']
    date = datetime.datetime.today()
    print 'date OK'
    entry = Entry(title=title, normalized_title=normalized_title,
                  tagline=tagline, body=body, date=date)
    print 'entry created'
    entry.save()
    print 'entry saved'
    return HttpResponse('success!')

def save_img(request):
    if not pass_ok(request.POST['password']):
        return HttpResponse('password failure!')
    print request.FILES
    f = request.FILES['file']
    destination = open(settings.CWD + '/../app/static/%s' % f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return HttpResponse('success!')

@csrf_exempt
def post(request):
    if request.method != 'POST':
        return HttpResponse('failure!')
    if request.META['CONTENT_TYPE'] == 'application/json':
        foo = save_entry(request)
        print 'foo is %s' % foo
        return foo
    elif request.META['CONTENT_TYPE'] == 'multipart/form-data; boundary=----------boundary----------':
        return save_img(request)
    else:
        return HttpResponse("Shit! That didn't work.")

def pass_ok(passhash):
    with open('./password') as passfile:
        word = passfile.read()
        passhash += '\n'
        return passhash == word
