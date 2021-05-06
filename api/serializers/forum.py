from rest_framework import serializers

from ..models.forum import Forum


class ForumSerializer(serializers.ModelSerializer):
    """Forum 论坛帖子序列化器"""

    author_username = serializers.CharField(source='author')
    author_is_p = serializers.CharField(source='author.is_p')
    author_is_oc = serializers.CharField(source='author.is_oc')
    author_is_admin = serializers.CharField(source='author.is_admin')

    class Meta:
        model = Forum
        fields = '__all__'
