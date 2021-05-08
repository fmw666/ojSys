from rest_framework import serializers

from ..models.problem import Problem


class ProblemSerializer(serializers.ModelSerializer):
    """Problem 例题序列化器"""

    header = serializers.CharField(source='get_header_display')
    alg_type = serializers.CharField(source='get_alg_type_display')
    ds_type = serializers.CharField(source='get_ds_type_display')

    class Meta:
        model = Problem
        # field = ['id', 'name', 'message', 'header', 'alg_type', 'ds_type', 'author']
        fields = '__all__'

