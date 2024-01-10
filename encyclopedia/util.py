
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
import re
from django.shortcuts import render
from django import forms
import os 


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(request,title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        value = f.read().decode("utf-8")
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": value
        })

    except FileNotFoundError:
        return HttpResponse(f"Page not found. You're search KEY = {title}", status=404)


def search(request):
    query = request.GET.get('q')
    try:
        f = default_storage.open(f"entries/{query}.md")
        value = f.read().decode("utf-8")
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": value
        })
    except :
        try:
            list=[]
            for filename in os.listdir("entries"):
                if re.search(query, filename):
                    #usare session !!!!!!!
                    list.append(filename)
            if len(list)==0:
                return HttpResponse(f"Page not found. You're search KEY = {query}", status=404)
            return render(request, "encyclopedia/entry.html", {
                        "list": list,
                       
                    })
        except:
            return HttpResponse(f"Page not found. You're search KEY = {query}", status=404)
  