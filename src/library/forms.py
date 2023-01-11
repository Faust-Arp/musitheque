from django import forms
from django.forms import inlineformset_factory

from library.models import Track, Album


class AlbumCreateForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5, required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['groupe'].readonly = True
        self.fields['genre_primary'].widget.attrs['multiselect-search'] = 'true'
        self.fields['genre_secondary'].widget.attrs['multiselect-search'] = 'true'
        self.fields['type_owned'].label = ''
        self.fields['type_owned'].widget.attrs['hidden'] = 'true'
        self.fields['owned'].widget.attrs['hidden'] = 'true'

    class Meta:
        model = Album
        fields = [
            "title",
            "groupe",
            "number_album",
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

    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5, required=False)
    number = forms.IntegerField(label="")

    def __init__(self, *args, **kwargs):
        super(TracksCreateForm, self).__init__(*args, **kwargs)
        self.fields["playlist"].widget.attrs["multiselect-search"] = "true"

    class Meta:
        model = Track
        fields = [
            "number",
            "title",
            "duration",
            "playlist",
            "rating",
            "favorite"
        ]

TracksCreateFormSet = inlineformset_factory(Album, Track, form=TracksCreateForm, extra=20,)
