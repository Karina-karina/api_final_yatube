from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ViewSetMixin

from .models import *
from .permissions import IsAuthorOrReadOnly
from .serializers import *


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        pk = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk)
        return post.comments.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk)
        serializer.save(author=self.request.user, post=post)


class GroupView(ViewSetMixin, generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)


class FollowView(ViewSetMixin, generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('user',)
    search_fields = ('=following__username', '=user__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
