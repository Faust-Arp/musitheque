from django import forms
from django.forms import inlineformset_factory

from library.models import Track, Album


class AlbumCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['groupe'].readonly = True

    class Meta:
        model = Album
        fields = [
            "title",
            "groupe",
            "date_released",
            "date_listened",
            "type_vocal",
            "type_album",
            "owned",
            "type_owned",
            "genre_primary",
            "genre_secondary",
            "rating",
            "thumbnail",
        ]

class TracksCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TracksCreateForm, self).__init__(*args, **kwargs)
        self.fields['album'].readonly = True

    class Meta:
        model = Track
        fields = [
            "number",
            "title",
            "album",
            "duration",
            "playlist",
            "favorite",
            "rating",
        ]


TracksCreateFormSet = inlineformset_factory(Album, Track, fields=[
            "number",
            "title",
            "album",
            "duration",
            "playlist",
            "favorite",
            "rating",
        ], extra=1,)
