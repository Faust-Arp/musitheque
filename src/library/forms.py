from datetime import date, datetime

from django import forms
from django.db.transaction import commit
from django.forms import inlineformset_factory

from library.models import Track, Album

class SearchForm(forms.Form):
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'placeholder': 'Rechercher',
                                                         'id': 'recherche'
                                                         }),
                           )

class AlbumForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5, required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['groupe'].readonly = True
        self.fields['genre_primary'].widget.attrs['multiselect-search'] = 'true'
        self.fields['date_rated'].widget = forms.HiddenInput()

    class Meta:
        model = Album
        fields = [
            "title",
            "groupe",
            "number_album",
            "tracks_number",
            "date_released",
            "date_listened",
            "type_album",
            "type_owned",
            "genre_primary",
            "rating",
            "comment",
            "thumbnail",
            "date_rated"
        ]

    def clean_date_rated(self):
        rating = self.cleaned_data.get("rating")

        if not rating:
            return self.cleaned_data.get("date_rated")

        if self.instance.pk:
            # édition
            if self.instance.rating in (None, 0) and rating > 0:
                return datetime.now()
            return self.instance.date_rated
        else:
            # création
            if rating > 0:
                return datetime.now()

        return self.cleaned_data.get("date_rated")

class TracksCreateForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5, required=False)
    number = forms.IntegerField(label="")
    disc = forms.IntegerField(initial=None, label="CD")

    def __init__(self, *args, **kwargs):
        super(TracksCreateForm, self).__init__(*args, **kwargs)
        self.fields["playlist"].widget.attrs["multiselect-search"] = "true"
        self.initial["disc"] = 1
        self.initial["type"] = "RG"

    class Meta:
        model = Track
        fields = [
            "disc",
            "number",
            "title",
            "type",
            "duration",
            "playlist",
            "rating",
            "favorite"
        ]

class TracksEditForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5, required=False)
    number = forms.IntegerField(label="")
    disc = forms.IntegerField(initial=None, label="CD")

    def __init__(self, *args, **kwargs):
        super(TracksEditForm, self).__init__(*args, **kwargs)
        self.fields["playlist"].widget.attrs["multiselect-search"] = "true"

    class Meta:
        model = Track
        fields = [
            "disc",
            "number",
            "title",
            "type",
            "duration",
            "playlist",
            "rating",
            "favorite"
        ]