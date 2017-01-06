from django.contrib.auth.models import User
from django import forms
from .models import Album, Photos


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['album_title', 'album_logo']


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = ['photo']
