from django.contrib import admin

from .models import User, UserMapNote, MapPinCoordinate


class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date_published")
    list_display_links = ("title", "description")
    search_fields = ("title",)


admin.site.register(User)
admin.site.register(UserMapNote, NoteAdmin)
admin.site.register(MapPinCoordinate)
