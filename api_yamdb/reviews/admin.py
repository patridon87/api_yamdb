from django.contrib import admin

from .models import User, Review, Comment, Category, Genre, Title

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
