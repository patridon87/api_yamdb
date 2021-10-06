from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import signUp, ReviewViewSet, CommentViewSet

router_v1 = SimpleRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', signUp, name='signup'),
    path('v1/', include(router_v1.urls)),
]
