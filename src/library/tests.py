import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from library.models import Playlist, ScListFollowUp


class PlaylistDetailViewTest(TestCase):
    def setUp(self):
        self.playlist = Playlist.objects.create(
            name="Test Playlist",
            type="G",
            color="#ffffff"
        )

    def test_playlist_detail_without_sc_data(self):
        url = reverse('library:playlist', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_sc_data'])
        self.assertEqual(response.context['sc_labels'], [])
        self.assertEqual(response.context['sc_views'], [])
        self.assertEqual(response.context['sc_likes'], [])
        self.assertEqual(response.context['sc_albums'], [])
        self.assertContains(response, "Aucune donnée disponible")

    def test_playlist_detail_with_sc_data(self):
        followup1 = ScListFollowUp.objects.create(
            playlist=self.playlist,
            new_views_number=100,
            new_likes_number=10,
            new_albums_number=5
        )
        followup2 = ScListFollowUp.objects.create(
            playlist=self.playlist,
            new_views_number=150,
            new_likes_number=15,
            new_albums_number=7
        )

        url = reverse('library:playlist', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_sc_data'])
        self.assertEqual(len(response.context['sc_labels']), 2)
        self.assertEqual(response.context['sc_views'], [100, 150])
        self.assertEqual(response.context['sc_likes'], [10, 15])
        self.assertEqual(response.context['sc_albums'], [5, 7])
        self.assertContains(response, "scChart")

    def test_playlist_detail_filters_data_older_than_one_year(self):
        old_followup = ScListFollowUp.objects.create(
            playlist=self.playlist,
            new_views_number=50,
            new_likes_number=2,
            new_albums_number=1
        )
        # Manually backdate the created record
        old_date = timezone.now() - datetime.timedelta(days=400)
        ScListFollowUp.objects.filter(pk=old_followup.pk).update(date_changed=old_date)

        url = reverse('library:playlist', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_sc_data'])
        self.assertEqual(response.context['sc_labels'], [])
