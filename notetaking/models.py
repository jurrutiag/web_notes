from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


class Color(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True, error_messages={'unique': '%(model_name)s tag already exist.'})
    color = models.ForeignKey(Color, on_delete=models.CASCADE, default="Gray")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('notetaking-home')


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default="No tag")
    date_created = models.DateTimeField(auto_now=True)
    is_pending = models.BooleanField(default=True)

    class Meta:
        unique_together = (('title', 'tag'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notetaking-home')
