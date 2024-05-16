from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, Textarea, TextInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.urls import reverse
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
import googlemaps

from .app_defaults import default_location
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
    return render(request, "mnotes/map3.html")


class NoteView(View):
    """A list of notes."""

    def get(self, request):
        template_name = "mnotes/notes.html"
        pins = request.user.map_pins.all()

        pk = request.user.pk
        avatar = SocialAccount.objects.get(user_id=pk).extra_data["photo"]

        locations = []
        for pin in pins:
            location = {
                "lat": pin.map_pin_point.x,
                "lng": pin.map_pin_point.y,
                "name": pin.title
            }
            locations.append(location)

        context = {"notes": pins,
                   "avatar": avatar,
                   "key": settings.GOOGLE_API_KEY,
                   "locations": locations
                   }

        return render(request, template_name, context)


class NoteCreateForm(ModelForm):
    class Meta:
        model = UserMapNote
        fields = ["title", "description", "map_pin_point"]
        widgets = {
            "description": Textarea(attrs={'rows': 5}),
            "map_pin_point": TextInput(attrs={'readonly': 'readonly', 'size': 38, 'style': 'text-align:center'})
        }


@login_required(redirect_field_name=None)
def note_create(request, note=None):
    is_edit = False
    location = default_location

    if request.method == "POST":
        form = NoteCreateForm(request.POST)
        cords = tuple(map(float, form["map_pin_point"].value().split(',')))
        info = {
            "title": form["title"].value(),
            "description": form["description"].value(),
            "map_pin_point": Point(cords, srid=4326)}
        if not note:
            note = UserMapNote.objects.create(**info)
            note.save()
            request.user.map_pins.add(note.pk)
        else:
            UserMapNote.objects.filter(pk=note.pk).update(**info)
        return redirect(reverse("notes"))

    else:
        form = NoteCreateForm()
        if note:
            form.fields['title'].initial = note.title
            form.fields['description'].initial = note.description
            form.fields['map_pin_point'].initial = f"{note.map_pin_point.x},{note.map_pin_point.y}"
            location["lat"] = note.map_pin_point.x
            location["lng"] = note.map_pin_point.y
            is_edit = True

    context = {
        "key": settings.GOOGLE_API_KEY,
        "location": location,
        "form": form,
        "is_edit": is_edit
    }
    return render(request, "mnotes/create.html", context)


@login_required(redirect_field_name=None)
def note_edit(request, pk=None):
    try:
        if request.user.map_pins.get(pk=pk):
            note = UserMapNote.objects.get(pk=pk)
            return note_create(request, note)
    except ObjectDoesNotExist:
        return redirect(reverse("notes"))


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

        location = {
            "lat": 56.8315958,
            "lng": 60.6076281,
            "name": "Heh"
        }
        context = {
            "note": user_note,
            "map_geo": map_geo_cords,
            "key": map_key,
            "location": location
        }

        return render(request, self.template_name, context)


class MapAdd(View):
    """A list of notes."""
    template_name = "mnotes/map3.html"

    def get(self, request):
        map_key = settings.GOOGLE_API_KEY
        user_note = UserMapNote.objects.all()
        # user_note_geo = MapPinCoordinate.objects.get(pk=pk)

        gmap = googlemaps.Client(key=map_key)
        map_default = gmap.geocode("Yekaterinburg, Sverdlovsk Oblast, Russia")
        map_geo_cords = list(map_default[0]["geometry"]["location"].values())
        map_geo_id = map_default[0]["place_id"]

        location = {
            "lat": 56.8315958,
            "lng": 60.6076281,
            "name": "Heh"
        }
        context = {
            "note": user_note,
            "map_geo": map_geo_cords,
            "key": map_key,
            "location": location
        }

        return render(request, self.template_name, context)
