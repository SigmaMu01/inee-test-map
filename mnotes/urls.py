from django.contrib.auth.decorators import login_required
from django.urls import path

from .app_defaults import NO_LOGIN_REDIRECT
from .views import NoteView, index, note_create, note_delete, note_edit


urlpatterns = [
    path("", index, name="index"),
    path(
        "notes/", login_required(NoteView.as_view(), **NO_LOGIN_REDIRECT), name="notes"
    ),
    path("notes/delete/<int:pk>", note_delete, name="note_delete"),
    path("notes/edit/<int:pk>", note_edit, name="note_edit"),
    path("notes/create", note_create, name="note_create"),
]
