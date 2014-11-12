from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    content = models.TextField()
    created = models.DateTimeField(db_index=True)
    tags = TaggableManager(blank=True)
    meta_desc = models.TextField(blank=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey('Category')
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.title

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return "%s" % self.name
