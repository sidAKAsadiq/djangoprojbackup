from rest_framework.serializers import ModelSerializer
from main.models import *

#   VERY SIMILAR TO MODEL FORMS

class room_serializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'