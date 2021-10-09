from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .pagination import TitlesPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsAdmin
from .serializers import (CategorySerializer, GenreSerializer, CommentSerializer,
                          TitleReadSerializer, TitleSerializer, ReviewSerializer,
                          UserSerializer,)
from reviews.models import (Comment, Category, Genre,
                            Title, User, Review)

from .serializers import UserRegistrationSerializer


@api_view(['POST'])
def signUp(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = serializer.instance
        token = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {token}',
            'yamdbSIA@gmail.com',
            [user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    if User.objects.filter(**request.data).exists():
        user = User.objects.get(**request.data)
        token = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {token}',
            'yamdbSIA@gmail.com',
            [user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def get_token(request):
    username=request.data.get('username')
    token = request.data.get('confirmation_code')
    if username is not None and token is not None:
        user = get_object_or_404(User, username=username)
   
        if default_token_generator.check_token(user, token):
            return Response(get_tokens_for_user(user))
        return Response(
            data='Код подтверждения не верный', 
            status=status.HTTP_400_BAD_REQUEST
            )
        
    return Response(
        data='Пользователь не найден', 
        status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAdmin,]
    http_method_names = ['get', 'post', 'patch', 'delete']

    

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
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year', ]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TitlesPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title__pk=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TitlesPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        serializer.save(author=self.request.user, review=review)
