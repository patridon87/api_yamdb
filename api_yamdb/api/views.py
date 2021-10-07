import random

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .pagination import TitlesPagination
from .permissions import SAFE_METHODS, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title

def signUp(request):
    pass


class ListCreateDestroyViewSet(GenericViewSet, CreateModelMixin,
                               DestroyModelMixin, ListModelMixin):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Get list of all categories.
    Only admin or moderator can create or delete category.
    Search by name of category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = TitlesPagination


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Get list of all genres.
    Only admin or moderator can create or delete genre.
    Search by name of genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = TitlesPagination


class TitleViewSet(ModelViewSet):
    """
    Get list of all titles.
    Only admin or moderator can create, edit or delete title.
    Filter by category, genre, title, year.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = TitlesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'title', 'year', ]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return TitleReadSerializer
        return TitleSerializer
