from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from .serializers import DeviceSeriakizer
from .models import Device

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSeriakizer

    def post(self, request, *args, **kwargs):
        # request.dataはapi経由で送られてくるデータ
        img = request.data['img']
        title = request.data['title']
        Device.objects.create(title=title, img=img)
        return HttpResponse({'message': 'New device create'}, status=200)
