from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from app.models import Entry
import datetime
import json

def main_page(request):
    entries = Entry.objects.order_by('-date')[:5]
    for entry in entries:
        print entry.date
    if datetime.date.today().year == 2012:
        date = '2012'
    else:
        date = '2012 -- %s' % datetime.date.today().year
    return render_to_response('blog.html',
                              {'entries': entries,
                               'date': date},
                              context_instance=RequestContext(request))

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

@csrf_exempt
def post(request):
    if request.method != 'POST':
        return HttpResponse('failure!')
    entry_data = json.load(request)
    passhash = entry_data['password']
    with open('./password') as passfile:
        if passhash != passfile.read():
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
