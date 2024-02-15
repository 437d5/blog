from django.urls import path

from . import views

app_name = "publications"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/comment/", views.comment, name="comment"),
    path("add_publication/", views.add_publication, name="add_publication"),
    path("<int:pk>/comment/del_comment/<int:comment_id>", views.del_comment, name="del_comment")
]
