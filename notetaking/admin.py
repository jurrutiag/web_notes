from django.contrib import admin
try:
    from notetaking.models import Note, Tag, Color

except:
    pass

admin.site.register(Note)
admin.site.register(Color)
admin.site.register(Tag)
