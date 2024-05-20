from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .app_defaults import NO_LOGIN_REDIRECT, default_location
from .forms import NoteCreateForm
from .models import UserMapNote


__all__ = ("HttpResponse",)  # Store unused functions here (flake8 dev guide)


def index(request):
    """
    Show index page with this web-service description or
    redirect authenticated user to a list of their notes.
    """
    if not request.user.is_authenticated:
        return render(request, "mnotes/index.html")
    else:
        return redirect(reverse("notes"))


def logout_view(request):
    """Immediate logout with no pop-ups."""
    logout(request)
    return index(request)


class NoteView(View):
    """A list of user notes with a map pointing to the last note address."""

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
                "name": pin.title,
            }
            locations.append(location)

        context = {
            "notes": pins,
            "avatar": avatar,
            "key": settings.GOOGLE_API_KEY,
            "locations": locations,
        }
        return render(request, template_name, context)


@login_required(**NO_LOGIN_REDIRECT)
def note_create(request, note=None):
    """Create a new user note or update already existing note."""
    is_edit = False
    location = default_location()

    if request.method == "POST":
        form = NoteCreateForm(request.POST)
        cords = tuple(map(float, form["map_pin_point"].value().split(",")))
        info = {
            "title": form["title"].value(),
            "description": form["description"].value(),
            "map_pin_point": Point(cords, srid=4326),
        }
        if not note:
            note = UserMapNote.objects.create(**info)
            note.save()
            request.user.map_pins.add(note.pk)
        else:
            UserMapNote.objects.filter(pk=note.pk).update(**info)
        return redirect(reverse("notes"))

    else:  # If method is GET then create an empty form
        form = NoteCreateForm()
        if note:  # If note is passed as argument then fill in the form (edit this note)
            form.fields["title"].initial = note.title
            form.fields["description"].initial = note.description
            form.fields["map_pin_point"].initial = (
                f"{note.map_pin_point.x},{note.map_pin_point.y}"
            )
            location["lat"] = note.map_pin_point.x
            location["lng"] = note.map_pin_point.y
            is_edit = True

    context = {
        "key": settings.GOOGLE_API_KEY,
        "location": location,
        "form": form,
        "is_edit": is_edit,
    }
    return render(request, "mnotes/create.html", context)


@login_required(**NO_LOGIN_REDIRECT)
def note_edit(request, pk=None):
    """
    Check if note exists and belongs to this user then call create
    function with existing note as argument.
    """
    try:
        if request.user.map_pins.get(pk=pk):
            note = UserMapNote.objects.get(pk=pk)
            return note_create(request, note)
    except ObjectDoesNotExist:
        return redirect(reverse("notes"))


@login_required(**NO_LOGIN_REDIRECT)
def note_delete(request, pk=None):
    """Check if note exists and belongs to this user then delete it."""
    try:
        if request.user.map_pins.get(pk=pk):
            note = UserMapNote.objects.get(pk=pk)
            note.delete()
    finally:
        return redirect(reverse("notes"))  # pylint: disable=W0134,W0150
