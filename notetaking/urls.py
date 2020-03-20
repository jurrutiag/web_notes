"""Map the requests to the corresponding response inside the app."""

from django.urls import path
from notetaking import views as note_views

urlpatterns = [
    path('', note_views.ListNoteView.as_view(), name='notetaking-home'),
    path('create/', note_views.CreateNoteView.as_view(), name='notetaking-create'),
    path('check_pending/<int:note_id>/', note_views.check_note, name='notetaking-check'),
    path('delete/<int:note_id>/', note_views.delete_note, name='notetaking-delete'),
    path('delete_non_pending/', note_views.delete_non_pending, name='notetaking-delete-nonpending')
]
