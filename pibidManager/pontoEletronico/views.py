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
from models import *
from forms import *

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
        return context;

    def form_valid(self, form):
        user = form.get_user()
        groups = user.groups.values_list('name',flat=True)
        if("Bolsista" in groups):
            if(self.registrarPresenca(user)):
                return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))
        return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))#seria pagina de erro

    '''
    Funcao responsavel pela presenca
    @TODO Nao identifique casos que a frequencia possa falhar
    '''
    def registrarPresenca(self, user):
        today = timezone.now()
        bolsista = Bolsista.objects.get(user=user)
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
            #presenca.save()
            #return True
        except :#Cria uma frequencia somente com a entrarda
            presenca = Presenca(bolsista=bolsista, data=today.date(), chegada=today.time(), frequencia=frequencia)
            #presenca.save()
            #return True
        presenca.save()
        return True

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
        return HttpResponseRedirect(reverse_lazy('pontoEletronico:index'))#Erro

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


class FrequenciaList(ListView):
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


class BolsistaDetail(DetailView):
    model = Bolsista
    template_name = 'bolsista_detail.html'

    def get_object(self, queryset=None):
        if(self.kwargs.get('pk',None)==u'-1'):
            return Bolsista.objects.get(user=self.request.user)
        return super(BolsistaDetail,self).get_object(queryset)

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
        return reverse_lazy('pontoEletronico:bolsistaList')

class BolsistaList(ListView,):
    model = Bolsista
    template_name = 'bolsista_list.html'


class PresencaCreate(CreateView):
    model = Presenca
    form_class = PresencaForm
    template_name = 'presenca_form.html'

    def get_success_url(self):
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


class PresencaUpdate(UpdateView):
    model = Presenca
    fields = '__all__'
    template_name = 'presenca_form.html'

    def get_success_url(self):
        return reverse_lazy('pontoEletronico:presencaList')


class PresencaList(ListView):
    model= Presenca
    template_name = 'presenca_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Presenca.objects.all().order_by('data').reverse()

class PresencaDelete(DeleteView):
    model = Presenca