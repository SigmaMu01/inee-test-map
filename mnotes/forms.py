"""Forms for user input data."""

from django.forms import ModelForm, Textarea, TextInput

from mnotes.models import UserMapNote


class NoteCreateForm(ModelForm):
    class Meta:
        model = UserMapNote
        fields = ["title", "description", "map_pin_point"]
        widgets = {
            "description": Textarea(attrs={"rows": 5}),
            "map_pin_point": TextInput(
                attrs={"readonly": "readonly", "size": 38, "style": "text-align:center"}
            ),
        }
