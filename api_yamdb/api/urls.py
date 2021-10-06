from django.urls import include, path
from rest_framework import routers

from . import views
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', views.signUp, name='signup'),
    path('v1/', include(router_v1.urls)),
]
