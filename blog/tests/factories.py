# -*- coding: utf-8 -*-
from datetime import datetime

import factory
from django.template.defaultfilters import slugify
from django_libs.tests.factories import UserFactory

from blog import models


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: "category_%d" % n)
    slug = factory.LazyAttribute(lambda n: slugify(n.name))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    title = factory.Sequence(lambda n: 'My {0} title'.format(n))
    category = factory.SubFactory(CategoryFactory)
    created = factory.LazyAttribute(lambda x: datetime.now())
    slug = factory.LazyAttribute(lambda n: slugify(n.title))
    author = factory.SubFactory(UserFactory)


class PublishedPostFactory(PostFactory):

    title = "Published Post"
    published = True


class UnPublishedPostFactory(PostFactory):

    title = "My Unpublished Post"
    published = False
