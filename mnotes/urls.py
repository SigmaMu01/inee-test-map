from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import NoteView, index, note_edit, note_create, note_delete
from .app_defaults import NO_LOGIN_REDIRECT


urlpatterns = [
    path("", index, name="index"),
    path(
        "notes/", login_required(NoteView.as_view(), **NO_LOGIN_REDIRECT), name="notes"
    ),
    path("notes/delete/<int:pk>", note_delete, name="note_delete"),
    path("notes/edit/<int:pk>", note_edit, name="note_edit"),
    path("notes/create", note_create, name="note_create"),
]
