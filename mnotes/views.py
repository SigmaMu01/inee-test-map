from django.http import HttpResponse

from .models import UserMapNote


def index(request):
    is_logged_in = True  # PASS
    if is_logged_in:
        return user_page()
    else:
        return welcome_page()


def welcome_page():
    return HttpResponse("Short service description.")


def user_page():
    has_memories = False  # PASS
    if UserMapNote.objects.count() > 0:
        return HttpResponse("Your memories here:")
    else:
        return HttpResponse("You don't have any memories yet.")
