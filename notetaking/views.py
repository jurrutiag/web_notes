from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from notetaking.forms import CreateNoteForm
from notetaking.models import Note
from django.shortcuts import redirect


class CreateNoteView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notetaking/create-note.html'
    form_class = CreateNoteForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListNoteView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notetaking/home.html'
    context_object_name = 'notes'
    ordering = ['-date_created']


def check_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.is_pending = not note.is_pending
    note.save()
    return redirect('notetaking-home')


def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('notetaking-home')


def delete_non_pending(request):
    notes = Note.objects.filter(is_pending=False)
    notes.delete()
    return redirect('notetaking-home')
