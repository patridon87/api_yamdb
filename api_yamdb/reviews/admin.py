from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"
    search_fields = ("name",)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"
    search_fields = ("name",)


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", "description")
    empty_value_display = "-пусто-"
    search_fields = ("name",)
    list_filter = ("category", "year", "genre")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author", "pub_date", "title", "score")
    empty_value_display = "-пусто-"
    search_fields = ("title",)
    list_filter = ("author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author", "pub_date", "review")
    empty_value_display = "-пусто-"
    search_fields = ("text",)
    list_filter = ("pub_date", "author")


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
