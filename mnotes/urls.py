from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path("", index),
    path("notes/", login_required(NoteView.as_view()), name="notes"),
    path("notes/delete/<int:pk>", note_delete, name="note_delete"),
    path("notes/edit/<int:pk>", note_edit, name="note_edit"),
    path("notes/create", note_create, name="note_create")
]
