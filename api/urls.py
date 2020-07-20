from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import CommentViewSet, FollowView, GroupView, PostViewSet

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    'comments')
v1_router.register('group', GroupView)
v1_router.register('follow', FollowView)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(v1_router.urls)),
]
