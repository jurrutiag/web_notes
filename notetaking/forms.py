from django.forms import CharField, ModelForm
from notetaking.models import Note


class CreateNoteForm(ModelForm):
    title = CharField(max_length=100, required=True)
    content = CharField(max_length=300, required=True)

    class Meta:
        model = Note
        fields = ['title', 'content']
