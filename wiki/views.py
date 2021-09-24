from django.shortcuts import render, redirect
from django import forms
from . import util
from random import randint
import re

from markdown2 import Markdown, markdown
from django.urls import reverse_lazy

markdowner = Markdown()

#class Post(forms.Form):
#    title = forms.CharField(label= "Title")
#    textarea = forms.CharField(widget=forms.Textarea(), label='')

#class Edit(forms.Form):
#    textarea = forms.CharField(widget=forms.Textarea(), label='')
    

def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries()
    })


# Search logic
def search(request):
    entries = util.list_entries()
    query = request.GET.get('q').lower()
    entry = [item.lower() for item in entries]
    searchlist = []
    for i in entry:
        if re.search(query, i):
            searchlist.append(i)
    #print(len(searchlist))
    
    if query:
        print(entry)
        if len(searchlist) == 0:
            return render(request, "wiki/error.html", {"message": "The search result not found Try again"})
        if len(searchlist) == 1:
            for pages in searchlist:
                page = util.get_entry(pages)
                page_converted = markdowner.convert(page)
                context = {
                    'page': page_converted,
                    'title': query,
                    }
                return render(request, "wiki/sing_search.html", context)
        if len(searchlist) > 1:
            #print(searchlist)
            return render(request, "wiki/search.html", {"entries": searchlist})
    else:
        return render(request, "wiki/error.html", {"message": "Type some thing in search"})

# Entry page 
def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        context = {
            'page': page_converted,
            'title': title,
        }
        return render(request, "wiki/entry.html", context)
    else:
        return render(request, "wiki/error.html", {"message": "The requested page was not found."})

#Creat New page entry
def add_page(request):
    entries = util.list_entries()
    title = request.POST.get("title")
    success_url = reverse_lazy('wiki:entry', kwargs={'title': title})

    if request.method == 'POST':
        if not title:
            return render(request, "wiki/error.html", {"message": "Please enter the title"})
        elif title in entries:
            return render(request, "wiki/error.html", {"message": "Page already exist chose another title"})
        else:
            util.save_entry(title, bytes(request.POST['content'], 'utf8'))

            return redirect(success_url)
    else:
        return render(request, "wiki/add_page.html")

def edit(request, title):
    entries = util.list_entries()
    success_url = reverse_lazy('wiki:entry', kwargs={'title': title})

    if request.method == 'GET':
        page = util.get_entry(title)
        context = {
            'title': title,
            'content': page
        }
        return render(request, "wiki/edit.html", context)
    elif request.method == 'POST':
        util.save_entry(title, bytes(request.POST['newcontent'], 'utf8'))
        return redirect(success_url)

def random(request):
    entries = util.list_entries()
    num = randint(0, len(entries) - 1)
    page_random = entries[num]
    
    page = util.get_entry(page_random)
    page_converted = markdowner.convert(page)
    context = {
        'page': page_converted,
        'title': page_random,
        }
    return render(request, "wiki/random.html", context)
