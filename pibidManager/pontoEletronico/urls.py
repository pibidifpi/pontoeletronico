__author__ = 'stepgalvao'
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(),name="index"),#Pagina inicial, registrar frenquencia

    url(r'^login/',LoginView.as_view(), name="login"),#Pagina de loging
    url(r'^logout/',auth_views.logout_then_login, name="logout"),#Necessario para o logout

    # -1 para informar a frequencia do usuario logado, somente bolsista
    url(r'^frequenciaDetail/(?P<pk>[0-9,-1]+)', FrequenciaDetail.as_view(), name="frequenciaDetail"),

    # Falta teriminar. Resumo das frequencias de um mes/ano por um bolsista
    url(r'^frequenciaResumo/', FrequenciaResumo.as_view(), name="frequenciaResumo"),
    url(r'^frequenciaList/', FrequenciaList.as_view(), name="frequenciaList"),

    # -1 para informar o usuario logado, somente bolsista
    url(r'^bolsistaDetail/(?P<pk>[0-9,-1]+)', BolsistaDetail.as_view(), name="bolsistaDetail"),
    url(r'^bolsistaList/', BolsistaList.as_view(), name="bolsistaList"),
    url(r'^bolsistaCreate/', BolsistaCreate.as_view(), name="bolsistaCreate"),
    url(r'^bolsistaUpdate/(?P<pk>[0-9,-1]+)', BolsistaUpdate.as_view(), name="bolsistaUpdate"),
    url(r'^bolsistaDelete/(?P<pk>[0-9,-1]+)', BolsistaDelete.as_view(), name="bolsistaDelete"),
    url(r'^bolsistaMeusDadosUpdate/(?P<pk>[0-9,-1]+)', BolsistaMeusDadosUpdate.as_view(), name="bolsistaMeusDadosUpdate"),

    url(r'^presencaList/', PresencaList.as_view(), name="presencaList"),
    url(r'^presencaCreate/', PresencaCreate.as_view(), name="presencaCreate"),
    url(r'^presencaUpdate/(?P<pk>[0-9,-1]+)', PresencaUpdate.as_view(), name="presencaUpdate"),
    url(r'^presencaDelete/(?P<pk>[0-9,-1]+)', PresencaDelete.as_view(), name="presencaDelete"),
    url(r'^registrarTarefa/(?P<pk>[0-9,-1]+)', RegistrarTarefa.as_view(), name="registrarTarefa"),
    
    url(r'^atividadeList/', AtividadeList.as_view(), name="atividadeList"),
    url(r'^atividadeCreate/', AtividadeCreate.as_view(), name="atividadeCreate"),
    url(r'^atividadeUpdate/(?P<pk>[0-9,-1]+)', AtividadeUpdate.as_view(), name="atividadeUpdate"),
    url(r'^atividadeDelete/(?P<pk>[0-9,-1]+)', AtividadeDelete.as_view(), name="atividadeDelete"),
    url(r'^atividadeListBolsista/', AtividadeListBolsista.as_view(), name="atividadeListBolsista"),
    url(r'^atividadeDetail/(?P<pk>[0-9,-1]+)', AtividadeDetail.as_view(), name="atividadeDetail"),
    
    url(r'^noticiaList/', NoticiaList.as_view(), name="noticiaList"),
    url(r'^noticiaCreate/', NoticiaCreate.as_view(), name="noticiaCreate"),
    url(r'^noticiaUpdate/(?P<pk>[0-9,-1]+)', NoticiaUpdate.as_view(), name="noticiaUpdate"),
    url(r'^noticiaDelete/(?P<pk>[0-9,-1]+)', NoticiaDelete.as_view(), name="noticiaDelete"),
    url(r'^noticiaListBolsista/', NoticiaListBolsista.as_view(), name="noticiaListBolsista"),
    url(r'^noticiaDetail/(?P<pk>[0-9,-1]+)', NoticiaDetail.as_view(), name="noticiaDetail"),

    url(r'^institucional/',InstitucionalView.as_view(), name="institucional"),
    url(r'^documentos/',DocumentosView.as_view(), name="documentos"),

    url(r'^relatorioPresenca/', RelatorioView.as_view(), name="relatorioPresenca"),
    url(r'^relatorioPresencaWord/', RelatorioPresencaWord.as_view(), name="relatorioPresencaWord"),
    url(r'^relatorio1/', TestePDF.as_view(), name="relatorio1"),

]