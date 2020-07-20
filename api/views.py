from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

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


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('user',)
    search_fields = ('=following__username', '=user__username')

    def create(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            username = self.request.data.get('following')
            if username is None or username == '':
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            following = get_object_or_404(User, username=username)
            follow = Follow.objects.filter(user=self.request.user,
                                           following=following).exists()
            if follow:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if self.request.user != following:
                    serializer.save(user=self.request.user, following=following)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
