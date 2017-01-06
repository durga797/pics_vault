from django.db import models
from django.contrib.auth.models import Permission, User


class Album(models.Model):
    user = models.ForeignKey(User)
    album_title = models.CharField(max_length=500)
    album_logo = models.FileField()

    def __str__(self):
        return self.album_title + ' - '+self.user.username


class Photos(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    photo_title = models.CharField(max_length=250)
    photo = models.FileField()

    def __str__(self):
        return self.photo_title
