from library.models import Band, Genre, Album, Track
from datetime import timedelta, datetime, date


def get_album_duration(id):

    track_list = Track.objects.filter(album=id)
    full_duration = timedelta(seconds=0)

    for track in track_list:
        full_duration += track.duration

    return full_duration


def get_album_owned_count_for_band(id):
    albums = Album.objects.filter(groupe=id).count
    print(albums)
    album_owned = Album.objects.filter(groupe=id, owned=True).count
    print(album_owned)

    return album_owned, albums


def get_band_count_by_country():

    # On récupère la liste de tous les groupes et on les tri par pays pour l'ordre du graphique
    bands = Band.objects.all().order_by('country')
    # On initialise le dictionnaire
    band_by_countries = {}

    # Pour chaque groupe dans la liste des groupes
    for band in bands:
        # Si le pays du groupe est déjà dans le dictionnaire
        if band.country in band_by_countries:
            # On augmente de 1 le nombre de groupe de ce pays
            band_by_countries[band.country] += 1
        else:
            # Sinon on ajoute le pays au dictionnaire avec la valeur 1
            band_by_countries[band.country] = 1

    # On tri le dictionnaire par valeur descendante avec le reverse à True
    sorted_band_by_countries = sorted(band_by_countries.items(), key=lambda x: x[1], reverse=True)
    # Comme sorted ramène une liste on converti la liste en dictionnaire
    ordered_dict = dict(sorted_band_by_countries)

    # On récupère les pays et le nombre de groupe avec les méthodes keys et values dans 2 listes distinctes
    countries, bands_number = zip(*ordered_dict.items())
    # On converti les deux listes en tuples pour qu'elle fonctionne avec chart.js
    list_countries = list(countries)
    list_bands_number = list(bands_number)

    return list_countries, list_bands_number


def get_album_by_released_year():

    albums = Album.objects.all().order_by('date_released')
    album_by_year = {}

    for album in albums:

        if album.date_released.year in album_by_year:
            album_by_year[album.date_released.year] += 1
        else:
            album_by_year[album.date_released.year] = 1

    years, albums_number = zip(*album_by_year.items())

    list_years = list(years)
    list_albums_number = list(albums_number)

    return list_years, list_albums_number


def get_album_by_released_decade():

    albums = Album.objects.all().order_by('date_released')
    album_by_decade = {}

    for album in albums:

        album_year = album.date_released.strftime("%Y")
        album_decade = album_year[:-1] + "0"

        if album_decade in album_by_decade:
            album_by_decade[album_decade] += 1
        else:
            album_by_decade[album_decade] = 1

    decades, albums_number = zip(*album_by_decade.items())

    list_decades = list(decades)
    list_albums_number = list(albums_number)

    return list_decades, list_albums_number


def get_album_by_primary_genre():

    albums = Album.objects.all()
    albums_by_primary_genre = {}

    for album in albums:

        album_list_genre = list(album.genre_primary.all())

        for genre in album_list_genre:
            str_genre= str(genre)
            if str_genre in albums_by_primary_genre:
                albums_by_primary_genre[str_genre] += 1
                print(albums_by_primary_genre)
            else:
                albums_by_primary_genre[str_genre] = 1

    genres, albums_number = zip(*albums_by_primary_genre.items())

    list_genres = list(genres)
    print(list_genres)
    list_albums_number = list(albums_number)
    print(list_albums_number)

    return list_genres, list_albums_number
