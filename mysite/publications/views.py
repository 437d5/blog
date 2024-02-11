from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Publication, Comment

def index(request):
    template_name = "publications/index.html"
    publications = Publication.objects.order_by("-pub_date")[:10]
    context = {
        "publications": publications
    }


    return render(request, template_name=template_name, context=context)

def detail(request, pk):
    # Try to get publication with pk or 404
    publication = get_object_or_404(Publication, pk=pk)
    # Pass the context to publication/detail.html
    publication = Publication.objects.get(pk=pk)
    text = publication.text
    title = publication.title
    pub_date = publication.pub_date
    comments = publication.comment_set.all()
    comment_num = len(comments)
    context = {
        "text": text,
        "title": title,
        "pub_date": pub_date,
        "publication": publication,
        "comment_num": comment_num
    }
    return render(request, "publications/detail.html", context=context)

def comment(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    comments = publication.comment_set.all()
    if not comments:
        return HttpResponse("No comments there yet")
    context = {
        "comments": comments,
        "pk": pk
    }
    return render(request, "publications/comments.html", context=context)

def add_comment(request, pk):
    publication = get_object_or_404(Publication, pk = pk)
    text = request.POST["text"]    
    new_comment = publication.comment_set.create(text=text)
    new_comment.save()

    return HttpResponseRedirect(reverse("publications:comment", args=(pk,)))

def add_publication(request):
    title = request.POST["title"]
    text = request.POST["text"]
    
    new_publication = Publication(title=title, text=text)
    new_publication.save()
    
    return HttpResponseRedirect(reverse("publications:index"))

def del_comment(request, comment_id, pk):
    comment_to_delete = get_object_or_404(Comment, pk=comment_id)
    if comment_to_delete:
        comment_to_delete.delete()
    return HttpResponseRedirect(reverse("publications:comment", args=(pk,)))
