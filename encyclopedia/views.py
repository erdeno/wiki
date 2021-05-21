from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
from random import randrange
from django import forms

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")

    entry = forms.CharField(widget=forms.Textarea, label="Entry")


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):

    for entry in util.list_entries():
        if title.lower() == entry.lower():
            mkdown = util.get_entry(entry)
            html_content = Markdown().convert(mkdown)
            return render(
                request,
                "encyclopedia/entry.html",
                {"title": entry, "content": html_content},
            )
    else:
        return render(request, "encyclopedia/404.html")


def search(request):
    query = request.GET.get("q")
    for entry in util.list_entries():
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", kwargs={"title": entry}))
    filtered = list(filter(lambda i: query.lower() in i.lower(), util.list_entries()))
    return render(request, "encyclopedia/search.html", {"entries": filtered})


def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            for e in util.list_entries():
                if title.lower() == e.lower():
                    return render(
                        request,
                        "encyclopedia/add.html",
                        {"form": form, "error": "The entry is already exists."},
                    )
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
        else:
            return render(request, "encyclopedia/add.html", {"form": form})
    return render(
        request,
        "encyclopedia/add.html",
        {
            "form": NewEntryForm(),
        },
    )


def random(request):
    rnd = randrange(len(util.list_entries()))
    title = util.list_entries()[rnd]
    return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))


def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    else:
        form = NewEntryForm(initial={"title": title, "entry": entry})
    return render(request, "encyclopedia/edit.html", {"title": title, "form": form})
