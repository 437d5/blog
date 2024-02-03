from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
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
    try:
        publication = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        raise Http404(f"The publication with {pk} as id does not exist.")
    # Pass the context to publication/detail.html
    publication = Publication.objects.get(pk=pk)
    text = publication.text
    title = publication.title
    pub_date = publication.pub_date
    context = {
        "text": text,
        "title": title,
        "pub_date": pub_date,
        "publication": publication
    }
    return render(request, "publications/detail.html", context=context)

def comment(request, pk):
    try:
        publication = Publication.objects.get(pk=pk)
        comments = publication.comment_set.all()
    except:
        return HttpResponse("No comments there yet")
    context = {
        "comments": comments,
        "pk": pk
    }
    return render(request, "publications/comments.html", context=context)

def add_comment(request, pk):
    try:
        publication = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        return HttpResponse("Publication doesn't exist")

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
    try:
        comment_to_delete = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponse("Comment doesn't exist")
    
    comment_to_delete.delete()
    return HttpResponseRedirect(reverse("publications:comment", args=(pk,)))
