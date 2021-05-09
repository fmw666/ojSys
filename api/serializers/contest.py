from rest_framework import serializers

from .problem import ProblemSerializer
from ..models.contest import Contest


class ContestSerializer(serializers.ModelSerializer):
    """Contest 比赛序列化器"""

    author_username = serializers.CharField(source='author.user')
    sign_up_start_date = serializers.DateTimeField()

    class Meta:
        model = Contest
        # field = ['id', 'name', 'message', 'header', 'alg_type', 'ds_type', 'author_username']
        fields = '__all__'
