from django.urls import path
from library.views import LibraryHome, BandCreate, BandEdit, BandDetail, BandDelete
from library.views import AlbumDelete, AlbumCreate, AlbumDetail, AlbumEdit
from library.views import TrackCreate

app_name = "library"

urlpatterns = [
    path('', LibraryHome.as_view(), name='home'),
    path('create-band', BandCreate.as_view(), name='create-band'),
    path('band/<str:slug>', BandDetail.as_view(), name='band'),
    path('edit-band/<str:slug>', BandEdit.as_view(), name='edit-band'),
    path('delete-band/<str:slug>', BandDelete.as_view(), name='delete-band'),
    path('create-album', AlbumCreate.as_view(), name='create-album'),
    path('album/<pk>', AlbumDetail.as_view(), name='album'),
    path('edit-album/<str:slug>', AlbumEdit.as_view(), name='edit-album'),
    path('delete-album/<str:slug>', AlbumDelete.as_view(), name='delete-album'),
    path('album/<int:pk>/create-tracks', TrackCreate.as_view(), name='create-tracks' ),
]