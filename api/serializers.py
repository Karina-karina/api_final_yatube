from rest_framework import serializers

from .models import Comment, Follow, Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.ReadOnlyField(source='group.username')

    class Meta:
        fields = '__all__'

        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.StringRelatedField()

    class Meta:
        fields = ('user', 'following',)
        model = Follow
