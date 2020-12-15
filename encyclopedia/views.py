from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms

import random
import markdown2

class WikiForm(forms.Form):
    title = forms.CharField(label="Title", min_length=2, max_length=20)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs=
        {"placeholder":"Use Markdown Syntax", "style":"height: 300px"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    entries = util.list_entries()
    if entry in entries:
        content = util.get_entry(entry)
        HTML_format = markdown2.markdown(content)
        return render(request, "encyclopedia/wiki.html", {
            "title":entry,
            "content":HTML_format
        })
    else:
        return HttpResponseRedirect("/error")

def error(request):
    return render(request, "encyclopedia/error.html")


def search(request):
    if request.method=="GET":
        query = request.GET.get("q")
        if query == "" or query is None:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

    if util.get_entry(query) is not None:
        return redirect(wiki, query)

    entries = util.list_entries()
    result = []
    for e in entries:
        if query.lower() in e.lower() or e.lower() in query.lower():
            result.append(e)
    return render(request, "encyclopedia/search.html",{
        "query": query,
        "result": result,
        "is_found" : len(result) > 0
    })

def new(request):
    if request.method=="POST":
        form = WikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title=title, content=content)
                return redirect(wiki, title)
            else:
                return render(request, "encyclopedia/new.html",{
                "form":form,
                "message": "Already Exist"
    })

    else:
        return render(request, "encyclopedia/new.html",{
        "form":WikiForm()
    })

def random_page(request):
    entries=util.list_entries()
    random_entry = random.choice(entries)
    return redirect(wiki, random_entry)

def edit(request, entry):
    content = util.get_entry(entry)
    if request.method=="POST":
        new_content = request.POST.get("content")
        util.save_entry(title=entry, content=new_content)
        return redirect(wiki, entry)

    if content:
        return render(request, "encyclopedia/edit.html",{
        "title": entry,
        "content" : util.get_entry(entry)
    })

    else:
        return HttpResponseRedirect(reverse('index'))
