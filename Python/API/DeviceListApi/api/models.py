from django.db import models

def load_path(instance, filename):
    return '/'.join(['image', str(instance.title)+str('.jpg')])

class Device(models.Model):
    title = models.CharField(max_length=30, blank=False)
    img = models.ImageField(blank=True, null=True, upload_to=load_path)
  
    def __str__(self):
        return self.title
