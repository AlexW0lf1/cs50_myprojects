from django.shortcuts import render
from django import forms
from . import util
import re
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        "cols": 50,
        "rows": 5,
    }))

class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        "cols": 50,
        "rows": 5,
    }))

def search(request):
    print(request.GET.get('q'))
    q = request.GET.get('q')
    entries = util.list_entries()
    if q in entries:
        return HttpResponseRedirect(reverse('entry', args=(q,)))
    results = []
    for entry in entries:
        if q in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search.html",{
        "results": results,
        "q": q,
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    # If we don't have entry with given title
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "title": title
        }, status=404)
    # Regexes built using https://regex101.com/
    # HTML Substitutions for headings
    pattern = r"^#(\s*[\w\s&\-]+)$"
    for i in range(1,7):
        h = pattern.replace("#", "#"*i)
        entry = re.sub(h, r"<h1>\1</h1>".replace("h1", f"h{i}"), entry, 0, re.MULTILINE)
    
    # HTML substitution for links
    sub = r"<a href='\2'>\1</a>"
    entry = re.sub(r"\[([\w\s]+)\]\(([\w/]*)\)", sub, entry, 0, re.MULTILINE)

    # HTML substitution for bold
    entry = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", entry, 0)

    # HTML substitution for list
    # Insert ul tags
    regex = r"((\*\s.+\n)+)"
    sub = r"<ul>\1</ul>"
    entry = re.sub(regex, sub, entry, 0, re.MULTILINE)
    # Insert li tags
    regex = r"\*\s(.+)\n"
    sub = "<li>\\1</li>"
    entry = re.sub(regex, sub, entry, 0)
    

    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title,
    })


def new(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": f"{title} page already exists",
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "error": "Invalid form data"
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(),
        "error": "",
    })

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(reverse("entry", args=(entry,)))


def edit(request, title):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
            })

    entry = util.get_entry(title)
    form = EditForm(initial={"content": entry})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form,
    })

