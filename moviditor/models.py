from django.db import models
from django.contrib.auth.models import User
from moviditor.logic.users_logic import get_deleted_stand_in_user
# Create your models here.

class AudioModel(models.Model):
    name = models.CharField(editable=False)
    audio = models.FileField(upload_to='audios')
    date_added = models.DateTimeField(auto_now_add=True)
    size = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_stand_in_user), editable=False)
    class Meta:
        verbose_name = 'Audio'
    def __str__(self) -> str:
        return self.name

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images')

class VideoModel(models.Model):
    name = models.CharField(editable=False)
    video = models.FileField(upload_to='videos')
    date_added = models.DateTimeField(auto_now_add=True)
    size = models.DecimalField(editable=False, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, editable=False, on_delete=models.SET(get_deleted_stand_in_user))
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
    def __str__(self) -> str:
        return self.name