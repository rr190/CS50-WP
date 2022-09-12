from django.shortcuts import render
from . import util

from django.http import HttpResponse
from markdown2 import Markdown

import random as rd

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request, message):

    return render(request, "encyclopedia/error.html", {
            "error_message": message,
            }) 

def wiki(request, entry):

    if util.get_entry(entry) != None:
        file = util.get_entry(entry)

        return render(request, "encyclopedia/wiki.html", {
            "entry": entry.upper(), "file": markdowner.convert(file)
            })

    else:
        return error(request, "Wiki does not have an article with this name.")

    return render(request, "encyclopedia/wiki.html")

def search(request):
    if request.method == "GET":
        q = request.GET["q"]

        entries = util.list_entries()
        n = len(entries)
        x = 0
        while x < n:

            if q.lower() == entries[x].lower():
                return render(request, "encyclopedia/wiki.html", { 
                    "entry": q.upper()
                    })
                break

            elif q.lower() not in entries[x].lower():
                entries.remove(entries[x])
                x -= 1
                n -= 1
            x += 1

        return render(request, "encyclopedia/index.html", {
        "entry": q, "entries" : entries
        })

def newpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        for each in util.list_entries():
            if title.lower() == each.lower():
                return error(request, f"{title.upper()} already exists.")
            
        content = request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", { 
            "entries":util.list_entries()
        })
    return render(request, "encyclopedia/newpage.html")

def edit(request, entry):

    if request.method == "POST":

        content = request.POST["content"]

        util.save_entry(entry, content)

        return wiki(request, entry)

    content = util.get_entry(entry)

    return render(request, "encyclopedia/edit.html", {
    "entry_title":entry, "entry_content": content
    })


def random(request):

    entries = util.list_entries()
    n_entries = len(entries)

    random_n = rd.randint(0, n_entries - 1)


    return wiki(request, entries[random_n])

    






