from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth import logout

import googlemaps
from django.conf import settings

from .models import UserMapNote, City


def index(request):
    return render(request, "mnotes/index.html")


def logout_view(request):
    logout(request)
    return index(request)


@login_required(redirect_field_name=None)
def open_map(request):
    return render(request, "mnotes/map.html")


class NoteView(ListView):
    """A list of notes."""
    template_name = "mnotes/notes.html"
    context_object_name = "notes"
    model = UserMapNote
    success_url = "/notes/"


@login_required(redirect_field_name=None)
def note_delete(request, pk=None):
    note = UserMapNote.objects.get(pk=pk)
    note.delete()
    return render(request, 'mnotes/notes.html')


class MapView(View):
    """A list of notes."""
    template_name = "mnotes/map2.html"

    def get(self, request):
        map_key = settings.GOOGLE_API_KEY
        user_note = UserMapNote.objects.all()
        # user_note_geo = MapPinCoordinate.objects.get(pk=pk)

        gmap = googlemaps.Client(key=map_key)
        map_default = gmap.geocode("Yekaterinburg, Sverdlovsk Oblast, Russia")
        map_geo_cords = list(map_default[0]["geometry"]["location"].values())
        map_geo_id = map_default[0]["place_id"]
        locations = [{
            "lat": float(map_geo_cords[0]),
            "lng": float(map_geo_cords[1]),
            "name": "Heh"
        }]
        context = {
            "note": user_note,
            "map_geo": map_geo_cords,
            "key": map_key,
            "locations": locations
        }

        return render(request, self.template_name, context)
