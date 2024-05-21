from allauth.account.views import LoginView
from django.test import TestCase
from django.urls import resolve, reverse

from mnotes.views import (
    NoteView,
    index,
    logout_view,
    note_create,
    note_delete,
    note_edit,
)


class TestUrls(TestCase):
    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_index_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout_view)


class TestUrlsMnotes(TestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)

    def test_notes_url_is_resolved(self):
        url = reverse("notes")
        self.assertEqual(resolve(url).func.view_class, NoteView)

    def test_note_delete_url_is_resolved(self):
        url = reverse("note_delete", args=["0"])
        self.assertEqual(resolve(url).func, note_delete)

    def test_note_edit_url_is_resolved(self):
        url = reverse("note_edit", args=["0"])
        self.assertEqual(resolve(url).func, note_edit)

    def test_note_create_url_is_resolved(self):
        url = reverse("note_create")
        self.assertEqual(resolve(url).func, note_create)
