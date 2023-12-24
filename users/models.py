from django.db import models
from django.contrib.auth.models import User
from project_moviditor.settings import MEDIA_ROOT
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    picture = models.ImageField(blank=True, upload_to=f'{MEDIA_ROOT}\\profile_pics')
    date_created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    about = models.CharField(max_length=255)
    age = models.DateField()