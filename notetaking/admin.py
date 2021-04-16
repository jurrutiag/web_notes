from django.contrib import admin
from notetaking.models import Note, Tag, Color


admin.site.register(Note)
admin.site.register(Color)
admin.site.register(Tag)
