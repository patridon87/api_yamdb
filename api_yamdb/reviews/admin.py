from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year',
        'category', 'genre')
    search_fields = ('name')
    list_filter = ('name', 'year', 'category', 'genre',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
