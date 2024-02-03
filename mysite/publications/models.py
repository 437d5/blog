from django.db import models

# Create your models here.
class Publication(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    #slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    text = models.TextField(max_length=900)
    pub_date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
