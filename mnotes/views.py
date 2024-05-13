from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ModelForm, Textarea
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.urls import reverse
import googlemaps
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from .models import UserMapNote


def index(request):
    if not request.user.is_authenticated:
        return render(request, "mnotes/index.html")
    else:
        return redirect(reverse("notes"))


def logout_view(request):
    logout(request)
    return index(request)


@login_required(redirect_field_name=None)
def open_map(request):
    return render(request, "mnotes/map.html")


class NoteView(View):
    """A list of notes."""
    def get(self, request):
        template_name = "mnotes/notes.html"
        pins = request.user.map_pins.all()
        pk = request.user.pk
        avatar = "static 'mnotes/avatar_def.jpg"
        avatar = SocialAccount.objects.get(user_id=pk).extra_data["photo"]
        context = {"notes": pins,
                   "avatar": avatar}
        return render(request, template_name, context)


class NoteCreate(ModelForm):
    class Meta:
        model = UserMapNote
        fields = ["title", "description"]
        widgets = {
            "description": Textarea()
        }


@login_required(redirect_field_name=None)
def note_create(request):
    if request.method == "POST":
        form = NoteCreate(request.POST)
        if form.is_valid():
            note = UserMapNote.objects.create(title=form["title"].value(),
                                              description=form["description"].value())
            note.save()
            request.user.map_pins.add(note.pk)
        return redirect(reverse("notes"))
    else:
        form = NoteCreate()
    return render(request, "mnotes/create.html", {"form": form})



@login_required(redirect_field_name=None)
def note_delete(request, pk=None):
    try:
        if request.user.map_pins.get(pk=pk):
            note = UserMapNote.objects.get(pk=pk)
            note.delete()
    finally:
        return redirect(reverse("notes"))


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
