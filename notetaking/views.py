from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from notetaking.forms import NoteForm, TagForm, FilterForm
from notetaking.models import Note, Tag
from django.shortcuts import redirect, reverse, Http404, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.template import loader


class CreateNoteView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    template_name = 'notetaking/create-edit-note.html'
    form_class = NoteForm
    success_message = "%(title)s note was created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        new_note = Note.objects.last()
        context = {
            'note': new_note,
            'pending': True,
        }

        note_template = loader.get_template('notetaking/note-template.html')
        message_template = loader.get_template('notetaking/message.html')

        response = {
            'note': note_template.render(context),
            'message': message_template.render({'message': list(messages.get_messages(self.request))[-1]}),
        }

        return JsonResponse(response)


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

        new_note_form = NoteForm()
        new_note_form.fields['content'].widget.attrs = {'rows': 2}
        del new_note_form.fields['content']

        new_tag_form = TagForm()

        context['filter_form'] = filter_form
        context['new_note_form'] = new_note_form
        context['new_tag_form'] = new_tag_form

        return context


class CreateTagView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    template_name = 'notetaking/create-edit-tag.html'
    form_class = TagForm
    success_message = "%(name)s tag was created successfully!"
    permission_denied_message = "hola"

    def form_invalid(self, form):
        super().form_invalid(form)

        message_template = loader.get_template('notetaking/message.html')
        messages.error(self.request, 'Tag name already exists.', extra_tags='danger')

        return JsonResponse({
            'message': message_template.render(context={'message': list(messages.get_messages(self.request))[-1]}),
            'valid': False,
        })

    def form_valid(self, form):
        super().form_valid(form)

        message_template = loader.get_template('notetaking/message.html')

        return JsonResponse({
            'tag_name': form.cleaned_data['name'],
            'message': message_template.render({'message': list(messages.get_messages(self.request))[-1]}),
            'valid': True,
        })


class EditTagView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = 'notetaking/create-edit-tag.html'
    form_class = TagForm


@login_required
def check_note(request):
    if 'note_id' in request.GET:
        note_id = request.GET['note_id']

    else:
        return Http404("Error, page does not exist")

    note = Note.objects.get(id=note_id)
    note.is_pending = not note.is_pending
    note.save()

    note_template = loader.get_template('notetaking/note-template.html')

    return JsonResponse({
        'note': note_template.render(context={'note': note}),
        'pending': note.is_pending,
    })


@login_required
def delete_note(request):
    if 'note_id' in request.GET:
        note_id = request.GET['note_id']

    else:
        return Http404("Error, page does not exist")

    note = Note.objects.get(id=note_id)
    note.delete()
    return HttpResponse("Success")


def delete_non_pending(request):
    notes = Note.objects.filter(is_pending=False)
    notes.delete()
    return HttpResponse("Success")

