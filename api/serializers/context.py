from rest_framework import serializers

from ..models.context import Context


class ContextSerializer(serializers.ModelSerializer):
    """Context 比赛序列化器"""

    author_username = serializers.CharField(source='author.user')

    class Meta:
        model = Context
        # field = ['id', 'name', 'message', 'header', 'alg_type', 'ds_type', 'author_username']
        fields = '__all__'
