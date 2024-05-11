from django.contrib import admin

from django.contrib.gis.admin import GISModelAdmin

from .models import User, UserMapNote, WorldBorder


class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date_published")
    list_display_links = ("title", "description")
    search_fields = ("title",)


admin.site.register(User)
admin.site.register(UserMapNote, NoteAdmin)
admin.site.register(WorldBorder, GISModelAdmin)
