from django.contrib import admin

from .models import User, Review, Comment

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
