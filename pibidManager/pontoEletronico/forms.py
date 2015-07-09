__author__ = 'stepgalvao'
from django.forms.models import *
from django.contrib.admin.widgets import *
from django.forms import widgets
from models import *


class PresencaForm(ModelForm):
    class Meta:
        model = Presenca
        fields = ['data','chegada','saida','bolsista']

    def __init__(self, *args, **kwargs):
        super(PresencaForm, self).__init__(*args, **kwargs)
        self.fields['chegada'].widget = AdminTimeWidget()
        self.fields['saida'].widget = AdminTimeWidget()
        self.fields['data'].widget = AdminDateWidget()