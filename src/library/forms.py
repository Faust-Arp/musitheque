from django import forms
from django.forms import inlineformset_factory

from library.models import Track, Album


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
