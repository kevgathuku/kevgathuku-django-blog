from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
