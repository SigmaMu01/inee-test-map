from allauth.socialaccount.models import SocialAccount
from django.contrib import auth
from django.contrib.gis.geos import Point
from django.test import Client, TestCase
from django.urls import reverse

from mnotes.models import User, UserMapNote


class TestNotes(TestCase):
    def setUp(self):
        """user1 has usermapnote1, usermapnote2; user2 has usermapnote3"""
        self.client = Client()

        self.user1_login = {"username": "biba", "password": "qweasd"}
        self.user2_login = {"username": "boba", "password": "qweasd2"}

        self.user1 = User.objects.create_user(**self.user1_login)
        self.user2 = User.objects.create_user(**self.user2_login)

        self.user1_vk = SocialAccount.objects.create(
            provider="vk",
            uid="000000001",
            extra_data={"photo": "avatar1.jpg"},
            user_id=self.user1.pk,
        )
        self.user2_vk = SocialAccount.objects.create(
            provider="vk",
            uid="000000002",
            extra_data={"photo": "avatar2.jpg"},
            user_id=self.user2.pk,
        )

        self.usermapnote1 = UserMapNote.objects.create(
            title="Test1",
            description="Simple Text",
            map_pin_point=Point(60.0, 60.0, srid=4326),
        )
        self.usermapnote2 = UserMapNote.objects.create(
            title="Test2",
            description="Simple Text",
            map_pin_point=Point(0.0, 30.0, srid=4326),
        )
        self.usermapnote3 = UserMapNote.objects.create(
            title="Test3",
            description="Simple Text",
            map_pin_point=Point(45.0, 15.0, srid=4326),
        )
        self.user1.map_pins.add(self.usermapnote1, self.usermapnote2)
        self.user2.map_pins.add(self.usermapnote3)

        self.user1_set = set(self.user1.map_pins.all())
        self.user2_set = set(self.user2.map_pins.all())
        # Get out-of-bounds pk for '_empty' tests
        self.latest_pk = int(UserMapNote.objects.latest("pk").pk) + 1

        self.index_url = reverse("index")
        self.note_create_url = reverse("note_create")
        self.note_edit_url = reverse("note_edit", args=[self.usermapnote3.pk])
        self.note_edit_empty_url = reverse("note_edit", args=[self.latest_pk])
        self.note_delete1_url = reverse("note_delete", args=[self.usermapnote1.pk])
        self.note_delete2_url = reverse("note_delete", args=[self.usermapnote3.pk])
        self.note_delete_empty_url = reverse("note_delete", args=[self.latest_pk])
        self.notes_url = reverse("notes")
        self.logout_url = reverse("logout")

    # ------------------------------ TEST AREA ------------------------------

    def test_mnotes_index_nologin(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mnotes/index.html")

    def test_mnotes_index_login(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.index_url)
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, "/notes/")

    def test_mnotes_logout(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.logout_url)
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mnotes/index.html")

    def test_mnotes_view1(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.notes_url)
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mnotes/notes.html")
        self.assertEqual(set(response.context["notes"]), self.user1_set)

    def test_mnotes_view2(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.notes_url)

        self.assertEqual(set(response.context["notes"]), self.user2_set)

    def test_mnotes_view_nouser(self):
        """Anonymous user attempts to open '/notes/' page."""
        response = self.client.get(self.notes_url)
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertRedirects(response, "/")

    def test_mnotes_view_wronguser1(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.notes_url)
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertFalse(set(response.context["notes"]).intersection(self.user1_set))

    def test_mnotes_view_wronguser2(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.notes_url)
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertFalse(set(response.context["notes"]).intersection(self.user2_set))

    def test_mnotes_view_empty(self):
        self.client.login(**self.user1_login)

    def test_mnotes_avatar1(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.notes_url)

        self.assertEqual(response.context["avatar"], "avatar1.jpg")

    def test_mnotes_avatar2(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.notes_url)

        self.assertEqual(response.context["avatar"], "avatar2.jpg")


class TestCreate(TestNotes):
    def test_mnotes_create(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.note_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mnotes/create.html")

    def test_mnotes_create_post(self):
        self.client.login(**self.user2_login)
        response = self.client.post(
            self.note_create_url,
            {
                "title": "New Title",
                "description": "New Description. New.",
                "map_pin_point": "15.0,15.0",
            },
        )
        usermapnote_new = UserMapNote.objects.latest("pk")

        self.assertTrue(len(self.user2_set) + 1 == len(set(self.user2.map_pins.all())))
        self.assertEqual(usermapnote_new.title, "New Title")
        self.assertRedirects(response, "/notes/")

    def test_mnotes_create_nouser(self):
        response = self.client.get(self.note_create_url)

        self.assertRedirects(response, "/")

    def test_mnotes_edit(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.note_edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mnotes/create.html")

    def test_mnotes_create_edit_post(self):
        self.client.login(**self.user2_login)
        response = self.client.post(
            self.note_edit_url,
            {
                "title": "New Title",
                "description": "New Description. New.",
                "map_pin_point": "15.0,15.0",
            },
        )
        usermapnote_new = UserMapNote.objects.get(pk=self.usermapnote3.pk)

        self.assertTrue(len(self.user2_set) == len(set(self.user2.map_pins.all())))
        self.assertEqual(usermapnote_new.title, "New Title")
        self.assertRedirects(response, "/notes/")

    def test_mnotes_edit_wronguser(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.note_edit_url)

        self.assertRedirects(response, "/notes/")

    def test_mnotes_edit_nouser(self):
        response = self.client.get(self.note_edit_url)

        self.assertRedirects(response, "/")

    def test_mnotes_edit_empty(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.note_delete_empty_url)

        with self.assertRaises(UserMapNote.DoesNotExist):
            UserMapNote.objects.get(pk=self.latest_pk)
        self.assertRedirects(response, "/notes/")


class TestDelete(TestNotes):
    def test_mnotes_delete(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.note_delete1_url)

        with self.assertRaises(UserMapNote.DoesNotExist):
            UserMapNote.objects.get(pk=self.usermapnote1.pk)
        self.assertRedirects(response, "/notes/")

    def test_mnotes_delete_empty(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.note_delete_empty_url)

        with self.assertRaises(UserMapNote.DoesNotExist):
            UserMapNote.objects.get(pk=self.latest_pk)
        self.assertRedirects(response, "/notes/")

    def test_mnotes_delete_wronguser1(self):
        self.client.login(**self.user2_login)
        response = self.client.get(self.note_delete1_url)

        self.assertTrue(UserMapNote.objects.get(pk=self.usermapnote1.pk))
        self.assertRedirects(response, "/notes/")

    def test_mnotes_delete_wronguser2(self):
        self.client.login(**self.user1_login)
        response = self.client.get(self.note_delete2_url)

        self.assertTrue(UserMapNote.objects.get(pk=self.usermapnote3.pk))
        self.assertRedirects(response, "/notes/")

    def test_mnotes_delete_nouser(self):
        response = self.client.get(self.note_delete2_url)

        self.assertTrue(UserMapNote.objects.get(pk=self.usermapnote3.pk))
        self.assertRedirects(response, "/")
