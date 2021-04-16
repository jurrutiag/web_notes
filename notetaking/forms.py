from django.forms import CharField, ModelForm, Textarea, ModelChoiceField, TextInput, Form
from notetaking.models import Note, Tag, Color

from django.core.exceptions import NON_FIELD_ERRORS


class NoteForm(ModelForm):
    title = CharField(max_length=100, required=True, widget=TextInput(attrs={'autofocus': 'autofocus', 'autocomplete': 'off'}))
    content = CharField(widget=Textarea(attrs={'autocomplete': 'off'}), max_length=300, required=False)
    tag = ModelChoiceField(Tag.objects)

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)

        self.last_note = Note.objects.last()
        if self.last_note is not None:
            self.last_tag = self.last_note.tag

        else:
            self.last_tag = Tag.objects.get(name="No tag")

        self.fields['tag'].initial = self.last_tag

    class Meta:
        model = Note
        fields = ['title', 'content', 'tag']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': '%(model_title)s note with %(model_tag)s tag already exist.',
            }
        }


class TagForm(ModelForm):
    name = CharField(max_length=100, required=True, widget=TextInput(attrs={'autocomplete': 'off'}))
    color = ModelChoiceField(Color.objects, initial=Color.objects.get(name="Gray"), required=True)

    class Meta:
        model = Tag
        fields = ['name', 'color']


class FilterForm(Form):
    tag_choice = ModelChoiceField(Tag.objects, empty_label="All", label="By Tag:", required=False)
