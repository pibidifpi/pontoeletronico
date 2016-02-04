
from django.forms.models import modelform_factory
from django.shortcuts import render
from django.views.generic import *
from django.forms.models import *
from django.views.generic.detail import *
from django.views.generic.edit import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from xdg.Exceptions import ValidationError
from models import *
from forms import *
from django.http import HttpResponse
from django.contrib import messages
from time import time,localtime
from pibid_relatorios.relatorio import *

#Teste Git
#Classes de restricoes das views


class CoordenadorRequiredMixi(object):
    @method_decorator(user_passes_test(lambda u: "Coordenador" in u.groups.values_list('name',flat=True)))
    def dispatch(self, *args, **kwargs):
        return super(CoordenadorRequiredMixi, self).dispatch(*args, **kwargs)


class BolsistaRequiredMixi(object):
    @method_decorator(user_passes_test(lambda u: ("Bolsista" in u.groups.values_list('name',flat=True)) or
                                                 ("Coordenador" in u.groups.values_list('name',flat=True))
                                       ))
    def dispatch(self, *args, **kwargs):
        return super(BolsistaRequiredMixi, self).dispatch(*args, **kwargs)


'''
Registro da presenca
Mostra uma a lista da ultimas 5 presencas atualizadas. Somente para bolsistas.
Caso a presenca do bolsista seja a primeira do mes ele criar um frequencia.
@TODO Pagina de erro: usuario e senha invalido ou usuario nao bolsista
'''
class IndexView(FormView):
    form_class = AuthenticationForm #Mesmo formulario do loging
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['object_list'] = Presenca.objects.all().order_by('atualizacao').reverse()[:5]
        context['noticia_list'] = Noticia.objects.all().order_by('data').reverse()[:5]
        return context;

    def form_valid(self, form):
        user = form.get_user()
        groups = user.groups.values_list('name',flat=True)
        if("Bolsista" in groups):
            retorno = self.registrarPresenca(user)
            if( retorno == 0):
                return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))
            else:
                return HttpResponseRedirect(reverse_lazy('pontoEletronico:registrarTarefa', kwargs={'pk':retorno}))

        messages.error(
            self.request,
            "Usuario invalido."
        )

        return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))#seria pagina de erro

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Username ou password invalidos."
        )
        return super(IndexView, self).form_invalid(form)


    '''
    Funcao responsavel pela presenca
    @TODO Nao identifique casos que a frequencia possa falhar
    '''
    def registrarPresenca(self, user):
        today = timezone.now()
        bolsista = Bolsista.objects.get(user=user)
        presencaId = 0

        #logica para montar a hora atual
        ano, mes, dia, hora, min, seg=localtime(time())[0:6]
        #fim da montagem da hora atual

        try:#Tenta pegar a frequencia do mes do bolsista
            frequencia = Frequencia.objects.get(bolsista=bolsista, mes=today.month, ano=today.year)
        except :#Cria uma nova frequencia caso nao exista
            frequencia = Frequencia(bolsista=bolsista, ano=today.year, mes=today.month)
            frequencia.save()
            #presenca = Presenca(bolsista=bolsista, data=today.date(), chegada=today, frequencia=frequencia)
            #presenca.save()
            #return True
        try:#Tenta pegar uma frequencia do dia com entrada. Registro de saida
            presenca = Presenca.objects.get(bolsista=bolsista, data=today.date(),saida=None)
            presenca.saida = today.time()
            """ estava bugando por causa do horario de verao
            horaAtual = str(hora)+":"+str(min)+":"+str(seg)
            presenca.saida = horaAtual
            """
            presencaId = presenca.id

            #presenca.save()
            #return True
        except :#Cria uma frequencia somente com a entrarda
            presenca = Presenca(bolsista=bolsista, data=today.date(), chegada=today.time(), frequencia=frequencia)

            """ estava bugando por causa do horario de verao
            horaAtual = str(hora)+":"+str(min)+":"+str(seg)
            presenca = Presenca(bolsista=bolsista, data=today.date(), chegada=horaAtual, frequencia=frequencia)
            """

            #presenca.save()
            #return True
        presenca.save()

        messages.success(
            self.request,
            "Registrado com sucesso."
        )
        return presencaId

'''
Login
@TODO nao tratei os logins invalidos
'''
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request,user)
        groups = user.groups.values_list('name',flat=True)
        if ("Bolsista" in groups):
            return HttpResponseRedirect(reverse_lazy('pontoEletronico:frequenciaDetail', kwargs={'pk':-1}))
        if("Coordenador" in groups):
            return HttpResponseRedirect(reverse_lazy('pontoEletronico:frequenciaResumo'))
        return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))#Erro
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Username ou password invalidos."
        )
        return super(LoginView, self).form_invalid(form)

'''
Resumo com as frequencias de um mes/ano.
Atualmente so mostra a do mes ano atual
'''
class FrequenciaResumo(ListView,CoordenadorRequiredMixi):
    model = Frequencia
    template_name = 'frequencia_resumo.html'
    mes = timezone.now().month
    ano = timezone.now().year

    def get_context_data(self, **kwargs):
        context = super(FrequenciaResumo,self).get_context_data(**kwargs)
        context['mes'] = self.mes
        context['ano'] = self.ano
        return context

    def get_queryset(self):
        return Frequencia.objects.filter(mes=self.mes,ano=self.ano)


class FrequenciaList(ListView, BolsistaRequiredMixi):
    template_name = 'frequencia_list.html'
    model = Frequencia

    def get_context_data(self, **kwargs):
        context = super(FrequenciaList,self).get_context_data()
        context['form']= modelform_factory(Frequencia, fields=['bolsista'])
        return context

    def get_queryset(self):
        bolsista = None
        if ("Bolsista" in self.request.user.groups.values_list('name',flat=True)):
            bolsista = Bolsista.objects.get(user=self.request.user)
        if('bolsista' in self.request.GET):
            bolsista = Bolsista.objects.get(id=self.request.GET['bolsista'])
        if(bolsista==None):
            return Frequencia.objects.all()
        return Frequencia.objects.filter(bolsista=bolsista)

class FrequenciaDetail(ListView,SingleObjectMixin):
    model = Presenca
    template_name = 'frequencia_detail.html'

    def get(self, request, *args, **kwargs):
        if(self.kwargs.get('pk',None)==u'-1'):
            bolsista = Bolsista.objects.get(user=request.user)
            frequencia = Frequencia.objects.get(bolsista=bolsista,mes=timezone.now().month)
            self.kwargs['pk']= frequencia.id
        self.object = super(FrequenciaDetail, self).get_object(queryset=Frequencia.objects.all())
        return super(FrequenciaDetail,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(FrequenciaDetail,self).get_context_data()
        context['object'] = self.object
        return context

    def get_queryset(self):
        return self.object.presenca_set.all()


class BolsistaDetail(DetailView, BolsistaRequiredMixi):
    model = Bolsista
    template_name = 'bolsista_detail.html'

    def get_object(self, queryset=None):
        if(self.kwargs.get('pk',None)==u'-1'):
            return Bolsista.objects.get(user=self.request.user)
        return super(BolsistaDetail,self).get_object(queryset)

class BolsistaMeusDadosUpdate(UpdateView, BolsistaRequiredMixi):
    model = Bolsista
    fields = ['nome','email', 'telefone']
    template_name = 'bolsista_form_update.html'

    def get_object(self, queryset=None):
        return Bolsista.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('pontoEletronico:bolsistaDetail', kwargs={'pk':-1})

class BolsistaUpdate(UpdateView,CoordenadorRequiredMixi):
    model = Bolsista
    fields = '__all__'
    template_name = 'bolsista_form.html'

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(
            self.request,
            "Atualizado com sucesso."
        )
        return reverse_lazy('pontoEletronico:bolsistaList')


class BolsistaCreate(CreateView,CoordenadorRequiredMixi):
    model = Bolsista
    template_name = 'bolsista_form.html'
    fields = ['nome','email', 'telefone']

    def get(self, request, *args, **kwargs):
        self.object=None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user_form = UserCreationForm()
        return self.render_to_response(self.get_context_data(form=form,user_form=user_form))

    def post(self, request, *args, **kwargs):
        self.object=None
        user_form = UserCreationForm(request.POST)
        formclass = self.get_form_class();
        form = self.get_form(formclass)
        if(form.is_valid() and user_form.is_valid()):
            return self.form_valid(form=form,user_form=user_form)
        else:
            return self.form_invalid(form=form,user_form=user_form)

    def form_valid(self, form, user_form):
        group = Group.objects.get(name="Bolsista")
        user = user_form.save()
        user.groups.add(group)
        user.save()
        self.object=form.save(commit=False)
        self.object.user = user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, user_form):
        return self.render_to_response(self.get_context_data(form=form,user_form=user_form))

    def get_success_url(self):
        messages.success(
            self.request,
            "Cadastrado com sucesso."
        )
        return reverse_lazy('pontoEletronico:bolsistaList')

class BolsistaDelete(DeleteView,CoordenadorRequiredMixi):
    model = Bolsista
    template_name = 'bolsista_confirm_delete.html'
    def get_success_url(self):
        messages.success(
            self.request,
            "Excluido com sucesso."
        )
        return reverse_lazy('pontoEletronico:bolsistaList')

class BolsistaList(ListView, CoordenadorRequiredMixi):
    model = Bolsista
    queryset = Bolsista.objects.all().order_by('id').reverse()
    template_name = 'bolsista_list.html'


class PresencaCreate(CreateView, CoordenadorRequiredMixi):
    model = Presenca
    form_class = PresencaForm
    template_name = 'presenca_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Cadastrado com sucesso."
        )

        return reverse_lazy('pontoEletronico:presencaList')

    def form_valid(self, form):
        self.object=form.save(commit=False)
        mes,ano,bolsista = self.object.data.month, self.object.data.year, self.object.bolsista
        try:
            frequencia=Frequencia.objects.get(mes=mes,ano=ano,bolsista=bolsista)
        except:
            frequencia = Frequencia(bolsista=bolsista,mes=mes,ano=ano)
            frequencia.save()
        frequencia.presenca_set.add(self.object)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PresencaUpdate(UpdateView, CoordenadorRequiredMixi):
    model = Presenca
    form_class = PresencaForm
    template_name = 'presenca_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Atualizado com sucesso."
        )
        return reverse_lazy('pontoEletronico:presencaList')


class PresencaList(ListView, CoordenadorRequiredMixi):
    model= Presenca
    template_name = 'presenca_list.html'

    def get_queryset(self):
        return Presenca.objects.all().order_by('data').reverse()

class PresencaDelete(DeleteView,CoordenadorRequiredMixi):
    model = Presenca
    template_name = 'presenca_confirm_delete.html'
    def get_success_url(self):
        messages.success(
            self.request,
            "Excluido com sucesso."
        )
        return reverse_lazy('pontoEletronico:presencaList')

class RegistrarTarefa(UpdateView, BolsistaRequiredMixi):
    model= Presenca
    form_class = RegistrarTarefaForm
    template_name = 'registrar_tarefa_form.html'

    def get_success_url(self):
        return reverse_lazy('pontoEletronico:index')
    

class AtividadeCreate(CreateView, CoordenadorRequiredMixi):
    model = Atividade
    form_class = AtividadeForm
    template_name = 'atividade_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Cadastrado com sucesso."
        )

        return reverse_lazy('pontoEletronico:atividadeList')


class AtividadeUpdate(UpdateView, CoordenadorRequiredMixi):
    model = Atividade
    form_class = AtividadeForm
    template_name = 'atividade_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Atualizado com sucesso."
        )
        return reverse_lazy('pontoEletronico:atividadeList')


class AtividadeList(ListView, CoordenadorRequiredMixi):
    model= Atividade
    template_name = 'atividade_list.html'

    def get_queryset(self):
        return Atividade.objects.all().order_by('data').reverse()

class AtividadeDelete(DeleteView,CoordenadorRequiredMixi):
    model = Atividade
    template_name = 'atividade_confirm_delete.html'
    def get_success_url(self):
        messages.success(
            self.request,
            "Excluido com sucesso."
        )
        return reverse_lazy('pontoEletronico:atividadeList')

class AtividadeListBolsista(ListView, BolsistaRequiredMixi):
    model= Atividade
    template_name = 'atividade_list_bolsista.html'

    def get_queryset(self):
        bolsista = Bolsista.objects.get(user=self.request.user)

        try:
            lista = Atividade.objects.filter(bolsistas=bolsista).order_by('data').reverse()
        except Atividade.DoesNotExist:
            lista = None

        return lista

class AtividadeDetail(DetailView, BolsistaRequiredMixi):
    model = Atividade
    template_name = 'atividade_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AtividadeDetail,self).get_context_data()
        bolsista = Bolsista.objects.get(user=self.request.user)

        try:
            context['object_list'] = Atividade.objects.filter(bolsistas=bolsista).order_by('data').reverse()[:5]
        except Atividade.DoesNotExist:
            context['object_list'] = None

        return context


class NoticiaCreate(CreateView, CoordenadorRequiredMixi):
    model = Noticia
    fields = '__all__'
    template_name = 'noticia_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Cadastrado com sucesso."
        )

        return reverse_lazy('pontoEletronico:noticiaList')


class NoticiaUpdate(UpdateView, CoordenadorRequiredMixi):
    model = Noticia
    fields = '__all__'
    template_name = 'noticia_form.html'

    def get_success_url(self):
        messages.success(
            self.request,
            "Atualizado com sucesso."
        )
        return reverse_lazy('pontoEletronico:noticiaList')


class NoticiaList(ListView, CoordenadorRequiredMixi):
    model= Noticia
    template_name = 'noticia_list.html'

    def get_queryset(self):
        return Noticia.objects.all().order_by('data').reverse()

class NoticiaDelete(DeleteView,CoordenadorRequiredMixi):
    model = Noticia
    template_name = 'noticia_confirm_delete.html'
    def get_success_url(self):
        messages.success(
            self.request,
            "Excluido com sucesso."
        )
        return reverse_lazy('pontoEletronico:noticiaList')

class NoticiaListBolsista(ListView, BolsistaRequiredMixi):
    model= Noticia
    template_name = 'noticia_list_bolsista.html'

    def get_queryset(self):
        return Noticia.objects.all().order_by('data').reverse()

class NoticiaDetail(DetailView, BolsistaRequiredMixi):
    model = Noticia
    template_name = 'noticia_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NoticiaDetail,self).get_context_data()
        context['object_list'] = Noticia.objects.all().order_by('data').reverse()[:5]
        return context

class InstitucionalView(TemplateView):
    template_name = 'institucional.html'

class DocumentosView(TemplateView):
    template_name = 'documentos.html'

class RelatorioView(FormView, CoordenadorRequiredMixi):
    form_class = RelatorioPresencaForm
    template_name = 'relatorio_presenca_form.html'

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Username ou password invalidos."
        )
        return super(RelatorioView, self).form_invalid(form)

class TestePDF(RelatoriosPDF, CoordenadorRequiredMixi):

    def dispatch(self, request, *args, **kwargs):
        self.novo_arquivo()
        self.abrir()
        self.seta(100, 100, 'Hello world.')
        self.imprimir()

        return self.response


class RelatorioPresencaWord(RelatoriosWord, CoordenadorRequiredMixi):
    nome_arquivo = 'relatorio_frequencia'
    titulo = 'CONTROLE DE FREQUENCIA DOS ALUNOS BOLSISTAS'
    cabecalho_tabela = ['Data','Entrada','Saida','Duracao','Atividade desenvolvida']

    def dispatch(self, request, *args, **kwargs):
        self.seta_listagem(request)
        self.construir_relatorio()

        return self.response

    def seta_listagem(self, request):

        condicao = '1=1'
        if request.POST.get('frequencia') != '':
            #condicao += ' and  MONTH(data) in (SELECT mes FROM pontoEletronico_frequencia where id = '+request.POST.get('frequencia')+') and YEAR(data) in (SELECT ano FROM pontoEletronico_frequencia where id = '+request.POST.get('frequencia')+') '
            condicao += ' and frequencia_id = '+request.POST.get('frequencia')

        if request.POST.get('bolsista') != '':
            condicao += ' and bolsista_id = '+request.POST.get('bolsista')

        self.listagem = Presenca.objects.raw('SELECT * FROM pontoEletronico_presenca where ' + condicao + ' order by bolsista_id, data desc')


    def construir_relatorio(self):

        lista = [[]] #criando uma matriz

        #logica do agrupamento da consulta por bolsista
        bolsista_atual = None
        contador_bolsistas = -1

        for presenca in self.listagem:

            if bolsista_atual != str(presenca.bolsista):
                bolsista_atual = str(presenca.bolsista)
                contador_bolsistas += 1

            """try:
                lista[contador_bolsistas].append(presenca)
            except :
                None"""

            lista[contador_bolsistas].append(presenca)

        #fim logica do agrupamento

        self.novo_arquivo()

        for bolsista in lista:

            if contador_bolsistas != -1:
                nome_bolsista = str(bolsista[0].bolsista)
            else:
                nome_bolsista = ''

            self.seta_agrupamento("Bolsista: " + nome_bolsista, 4)
            self.abrir_tabela()

            for presenca in bolsista:
                self.seta_linha([str(presenca.data), str(presenca.chegada), str(presenca.saida),
                                str(presenca.duracao), str(presenca.atividade.encode('utf-8'))])

            self.fechar_tabela()
            self.quebrar_linha()

