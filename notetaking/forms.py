from django.forms import CharField, ModelForm, Textarea
from django.contrib.auth.models import User
from notetaking.models import Note


class CreateNoteForm(ModelForm):
    title = CharField(max_length=100, required=True)
    content = CharField(widget=Textarea, max_length=300, required=False)

    class Meta:
        model = Note
        fields = ['title', 'content']
