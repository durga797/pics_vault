from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, AlbumForm, PhotoForm
from django.views.generic import View
from .models import Album, Photos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'str']


def home(request):
    return render(request, 'gallery/open.html')


class Register(View):
    form_class = UserForm
    template_name = 'gallery/signup.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            users = User.objects.all()
            for s in users:
                if s.email == form.cleaned_data.get("email"):
                    context = {
                        'users': users,
                        'form': form,
                        'error_message': 'That email id is already registered',
                    }
                    return render(request, 'gallery/signup.html', context)
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('gallery:index')

        return render(request, self.template_name, {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'gallery/index.html', {'albums': albums})
            else:
                return render(request, 'gallery/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'gallery/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gallery/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'gallery/open.html', context)


@login_required(login_url='/home/login')
def index(request):
    if request.user.is_authenticated():
        albums = Album.objects.filter(user=request.user)
        return render(request, 'gallery/index.html', {'albums': albums})
    else:
        return render(request, 'gallery/login.html')


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            albums = Album.objects.all()
            for s in albums:
                if s.album_title == form.cleaned_data.get("album_title"):
                    context = {
                        'album': albums,
                        'form': form,
                        'error_message': 'You already have an album with that name',
                    }
                    return render(request, 'gallery/create_album.html', context)
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, JPEG, GIF',
                }
                return render(request, 'gallery/create_album.html', context)
            album.save()
            return render(request, 'gallery/photos.html', {'albums': album})
        context = {
            "form": form,
        }
        return render(request, 'gallery/create_album.html', context)


def add_photo(request, album_id):
    form = PhotoForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_photos = album.photos_set.all()
        for s in albums_photos:
            if s.photo_title == form.cleaned_data.get("photo_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already have a photo with that name',
                }
                return render(request, 'gallery/create_photo.html', context)
        photo = form.save(commit=False)
        photo.album = album
        photo.photo = request.FILES['photo']
        photo.file_type = photo.photo.url.split('.')[-1]
        file_type = photo.file_type.lower()
        x = photo.photo.url.split('.')[0]
        y = x.split('media/')[-1]
        photo.photo_title = y
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, JPEG, GIF',
            }
            return render(request, 'gallery/create_photo.html', context)

        photo.save()
        return render(request, 'gallery/photos.html', {'albums': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'gallery/create_photo.html', context)


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'gallery/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        albums = Album.objects.filter(user=request.user)
        user1 = album.user
        if user == user1:
            return render(request, 'gallery/photos.html', {'albums': album, 'user': user})
        else:
            context = 'This album does not belong to you'
            return render(request, 'gallery/index.html', {'albums': albums,'error_message': context})


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'gallery/index.html', {'albums': albums})


def delete_photo(request, album_id, photo_id):
    album = get_object_or_404(Album, pk=album_id)
    photo = Photos.objects.get(pk=photo_id)
    photo.delete()
    return render(request, 'gallery/photos.html', {'albums': album})


def photo_view(request, album_id, photo_id):
    photo = Photos.objects.get(pk=photo_id)
    album = Album.objects.get(pk=album_id)
    photos = album.photos_set.all()
    return render(request, 'gallery/viewphoto.html', {'photo': photo, 'all_photos': photos})


def slide_show(request, album_id):
    user = request.user
    album = Album.objects.get(pk=album_id)
    albums = Album.objects.filter(user=request.user)
    user1 = album.user
    if user == user1:
        return render(request, 'gallery/slideshow.html', {'album': album, 'user': user})
    else:
        context = 'This album does not belong to you'
        return render(request, 'gallery/index.html', {'albums': albums, 'error_message': context})
