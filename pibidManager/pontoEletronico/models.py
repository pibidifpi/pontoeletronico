from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,Group

# Create your models here.
class Bolsista(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    user = models.OneToOneField(User,related_name='+') #User doesn't has Bolsista

    def __str__(self):
        return self.nome.encode('utf-8')


class Presenca(models.Model):
    bolsista = models.ForeignKey('Bolsista')
    data = models.DateField(default=timezone.now)
    chegada = models.TimeField()
    saida = models.TimeField(null=True)
    frequencia = models.ForeignKey('Frequencia')
    atualizacao = models.DateTimeField(auto_now=True)
    atividade = models.TextField(verbose_name='Atividade', null=True)

    def duracao(self):
        if self.saida == None:
            return timezone.timedelta()
        agora = timezone.now()
        chegada = timezone.datetime(year=agora.year,month=agora.month,day=agora.month,hour=self.chegada.hour, minute=self.chegada.minute)
        saida = timezone.datetime(year=agora.year,month=agora.month,day=agora.month,hour=self.saida.hour, minute=self.saida.minute)
        return saida-chegada

    def __str__(self):
        return self.bolsista.nome.encode('utf-8')+"-"+self.data.__str__()


class Frequencia(models.Model):
    bolsista = models.ForeignKey('Bolsista')
    mes = models.SmallIntegerField()
    ano = models.SmallIntegerField()
    atualizacao = models.DateTimeField(auto_now=True)

    def carga_horaria(self):
        total = timezone.timedelta()
        for p in self.presenca_set.all():
            total += p.duracao()
	    #79200 segundos = 22h
       	if(total.total_seconds() >= 79200) :
            total = total + timezone.timedelta(hours=8)

        return total

    def __str__(self):
        return self.bolsista.nome.encode('utf-8')+"-"+self.mes.__str__()+"/"+self.ano.__str__()
