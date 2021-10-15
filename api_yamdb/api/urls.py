from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
    sign_up,
)

router_v1 = SimpleRouter()


router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

router_v1.register(r"users/<username: str>", UserViewSet, basename="users")

urlpatterns = [
    path("v1/auth/signup/", sign_up, name="signup"),
    path("v1/auth/token/", get_token, name="get_token"),
    path("v1/", include(router_v1.urls)),
]
