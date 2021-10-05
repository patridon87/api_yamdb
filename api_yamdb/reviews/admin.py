from django.contrib import admin

from .models import Review, Comment

admin.site.register(Comment)
admin.site.register(Review)