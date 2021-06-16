# rest_framework
from rest_framework import serializers

# models
from ..models.forum import Forum


class ForumSerializer(serializers.ModelSerializer):
    """Forum 论坛帖子序列化器"""

    author_username = serializers.CharField(source='author')
    author_is_p = serializers.CharField(source='author.is_p')
    author_is_o = serializers.CharField(source='author.is_o')
    author_is_admin = serializers.CharField(source='author.is_admin')

    class Meta:
        model = Forum
        fields = '__all__'
