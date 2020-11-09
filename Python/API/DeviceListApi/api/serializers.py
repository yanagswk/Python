from rest_framework import serializers
from .models import Device

class DeviceSeriakizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'title', 'img']

