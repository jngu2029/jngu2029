from django.shortcuts import render, redirect
import random
from . import util
from markdown2 import Markdown

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    content = util.get_entry(title)
    converted_content = markdowner.convert(content) if content else None
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error_code": 404,
            "message": f"The requested page '{title}' was not found."
        }, status=404)
    else:
        return render(request, "encyclopedia/wiki.html", {
            "content": converted_content,
            "title": title
        })

def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()
    lowercase_entries = [entry.lower() for entry in entries]
    if query.lower() in lowercase_entries:
        return render(request, "encyclopedia/wiki.html", {
            "content": markdowner.convert(util.get_entry(query)),
            "title": query
        })
    else:
        #make a loop through each entry in the list of entries and check if the query is a substring of the entry
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "results": results,
            "query": query
            })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        #after getting the title, check if the title is empty or not
        if title:
            #check if title already exists in list of entries
            if title in util.list_entries():
                #if so, return an error message
                return render(request, "encyclopedia/error.html", {
                    "error_code": 400,
                    "message": f"The page '{title}' already exists."
                    }, status=400)
                
            #otherwise, create a new entry with the title and empty content
            util.save_entry(title, "")
            return render(request, "encyclopedia/wiki.html", {
                "title" : title,
                "content" : util.get_entry(title)
        })
            
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        util.save_entry(title, content)
        return redirect("wiki", title=title)
        
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : content
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    converted_content = markdowner.convert(util.get_entry(random_title))
    return render(request, "encyclopedia/wiki.html", {
        "content": converted_content,
        "title": random_title
    })