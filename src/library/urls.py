from django.urls import path
from library.views import BandList, BandCreate, BandEdit, BandDetail, BandDelete
from library.views import AlbumList, AlbumDelete, AlbumCreate, AlbumDetail, AlbumEdit
from library.views import TrackCreate

app_name = "library"

urlpatterns = [
    path('bands', BandList.as_view(), name='bands-list'),
    path('albums', AlbumList.as_view(), name='albums-list'),
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