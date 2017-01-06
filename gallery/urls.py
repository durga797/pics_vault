from django.conf.urls import url
from . import views

app_name = 'gallery'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^index$', views.index, name="index"),
    url(r'^login$', views.login_user, name="login"),
    url(r'^logout$', views.logout_user, name="logout"),
    url(r'^signup$', views.Register.as_view(), name="signup"),
    url(r'^album/add/$', views.create_album, name="create_album"),
    url(r'^(?P<album_id>[0-9]+)/delete/$', views.delete_album, name="delete_album"),
    url(r'^(?P<album_id>[0-9]+)/detail/$', views.detail, name="photos"),
    url(r'^(?P<album_id>[0-9]+)/slideshow/$', views.slide_show, name="slide_show"),
    url(r'^(?P<album_id>[0-9]+)/photo/(?P<photo_id>[0-9]+)/delete/$', views.delete_photo, name="delete_photo"),
    url(r'^album/(?P<album_id>[0-9]+)/add-photo$', views.add_photo, name="add_photo"),
    url(r'^(?P<album_id>[0-9]+)/photo/(?P<photo_id>[0-9]+)/detail/$', views.photo_view, name="photo_detail"),
]
