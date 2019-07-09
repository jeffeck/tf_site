from rest_framework import routers, serializers, viewsets
from .models import Iris


# Serializers define the API representation.
# class IrisSerializer(serializers.HyperlinkedModelSerializer):
class IrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iris
        fields = ('id', 'classification', 'sepal_length', 'sepal_width', 'petal_width', 'petal_length',) # 'url')

