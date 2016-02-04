__author__ = 'stepgalvao'
from django.forms.models import *
from django.contrib.admin.widgets import *
from django.forms import widgets
from models import *

class PresencaForm(ModelForm):
    class Meta:
        model = Presenca
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PresencaForm, self).__init__(*args, **kwargs)
        self.fields['chegada'].widget = AdminTimeWidget()
        self.fields['saida'].widget = AdminTimeWidget()
        self.fields['data'].widget = AdminDateWidget()

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AtividadeForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget = AdminDateWidget()

class RegistrarTarefaForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super (RegistrarTarefaForm,self ).__init__(*args,**kwargs) # populates the post

    class Meta:
        model = Presenca
        fields = ['atividade','tarefa']

class RelatorioPresencaForm(ModelForm):
    class Meta:
        model = Presenca
        fields = ['frequencia']