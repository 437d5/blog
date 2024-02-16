from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Publication, Comment
from .forms import CreatePublicatonsForm, CreateCommentsForm


def index(request):
    template_name = "publications/index.html"
    publications = Publication.objects.order_by("-pub_date")[:10]
    context = {
        "publications": publications
    }

    if request.method == "POST":
        form = CreatePublicatonsForm(request.POST)
        context["form"] = form
        title = request.POST.get("title")
        text = request.POST.get("text")
        new_publication = Publication(title=title, text=text)
        new_publication.save()
        return HttpResponseRedirect(reverse("publications:index"))
    else:
        form = CreatePublicatonsForm()
        context["form"] = form

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
    context = {
        "comments": comments,
        "pk": pk
    }
    if request.method == "POST":
        form = CreateCommentsForm(request.POST)
        context["form"] = form
        if form.is_valid():
            text = form.cleaned_data["text"]
            new_comment = publication.comment_set.create(text=text)
            new_comment.save()
        return HttpResponseRedirect(reverse("publications:comment", kwargs={"pk": pk}))
    else:
        form = CreateCommentsForm()
        context["form"] = form
        return render(request, "publications/comments.html", context=context)

def del_comment(request, comment_id, pk):
    comment_to_delete = get_object_or_404(Comment, pk=comment_id)
    if comment_to_delete:
        comment_to_delete.delete()
    return HttpResponseRedirect(reverse("publications:comment", args=(pk,)))

