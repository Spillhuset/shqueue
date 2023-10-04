from django import forms
from .models import *

class AddPersonToQueueForm(forms.ModelForm):
  class Meta:
    model = QueuedPerson
    fields = ['name']
