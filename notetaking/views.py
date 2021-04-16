from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView


from django.shortcuts import redirect, reverse, Http404, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.template import loader
from django.db.utils import OperationalError

try:
    from notetaking.forms import NoteForm, TagForm, FilterForm
    from notetaking.models import Note, Tag

except OperationalError:
    Note = None
    Tag = None
    NoteForm = None
    TagForm = None
    FilterForm = None



def get_messages(form, request, error=True):
    message_template = loader.get_template('notetaking/message.html')

    if error:
        for err_src, err_list in form.errors.items():
            for err in err_list:
                messages.error(request, err)

    return [message_template.render(context={'message': msg}) for msg in messages.get_messages(request)]


class CreateNoteView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    template_name = 'notetaking/create-edit-note.html'
    form_class = NoteForm
    success_message = "%(title)s note was created successfully!"

    def form_invalid(self, form):
        super().form_invalid(form)
        final_messages = get_messages(form, self.request, error=True)
        return JsonResponse({'messages': final_messages}, status=400)

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        new_note = Note.objects.last()
        context = {
            'note': new_note,
            'pending': True,
        }

        note_template = loader.get_template('notetaking/note-template.html')
        final_messages = get_messages(form, self.request, error=False)

        response = {
            'note': note_template.render(context),
            'messages': final_messages,
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

    def form_invalid(self, form):
        super().form_invalid(form)
        final_messages = get_messages(form, self.request, error=True)
        return JsonResponse({
            'messages': final_messages,
        }, status=400)

    def form_valid(self, form):
        super().form_valid(form)
        final_messages = get_messages(form, self.request, error=False)
        return JsonResponse({
            'tag_name': form.cleaned_data['name'],
            'messages': final_messages,
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


def search_note(is_pending):

    @login_required
    def wrapper(request):
        val = request.POST['search_text'] or ""
        passed_notes = Note.objects.filter(title__contains=val, is_pending=is_pending)
        note_template = loader.get_template('notetaking/note-template.html')

        html_notes = [note_template.render(context={"note": note}) for note in passed_notes]

        return JsonResponse({
            "results": html_notes,
        })

    return wrapper


@login_required
def delete_non_pending(request):
    notes = Note.objects.filter(is_pending=False)
    notes.delete()
    return HttpResponse("Success")

