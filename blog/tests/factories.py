# -*- coding: utf-8 -*-
from datetime import datetime

import factory
from django.template.defaultfilters import slugify
from django_libs.tests.factories import UserFactory

from blog import models


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: "user_%d" % n)
    slug = factory.Sequence(lambda n: "slug-%s" % n)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    category = factory.SubFactory(CategoryFactory)
    created = factory.LazyAttribute(lambda x: datetime.now())
    slug = factory.Sequence(lambda n: slugify(n))
    author = factory.SubFactory(UserFactory)


class PublishedPostFactory(PostFactory):

    title = "Published Post"
    published = True


class UnPublishedPostFactory(PostFactory):

    title = "My Unpublished Post"
    published = False
