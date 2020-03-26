from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from notetaking.forms import NoteForm, TagForm, FilterForm
from notetaking.models import Note, Tag
from django.shortcuts import redirect, render


class CreateNoteView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    template_name = 'notetaking/create-edit-note.html'
    form_class = NoteForm
    success_message = "%(title)s note was created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditNoteView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notetaking/create-edit-note.html'
    form_class = NoteForm


class HomeView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notetaking/home.html'
    context_object_name = 'notes'
    ordering = ['-date_created']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        filter_form = FilterForm()
        filter_form.fields['tag_choice'].initial = self.request.GET.get('tag', "")
        context['filter_form'] = filter_form

        return context


class CreateTagView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'notetaking/create-edit-tag.html'
    form_class = TagForm


class EditTagView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = 'notetaking/create-edit-tag.html'
    form_class = TagForm


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
