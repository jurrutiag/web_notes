from django.shortcuts import render

# Create your views here.


def create_note(request):
    from notetaking.models import Note
    from notetaking.forms import CreateNoteForm

    context = {
        'form': CreateNoteForm(),
        'notes': Note.objects.all(),
    }
    return render(request, 'notetaking/create-note.html', context)

def login(request):
    return render(request, 'notetaking/login.html')
