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
    url(r'^coordenadorBolsistaUpdate/(?P<pk>[0-9,-1]+)', CoordenadorBolsistaUpdate.as_view(), name="coordenadorBolsistaUpdate"),

    url(r'^bolsistaDelete/(?P<pk>[0-9,-1]+)', BolsistaDelete.as_view(), name="bolsistaDelete"),

    url(r'^presencaList/', PresencaList.as_view(), name="presencaList"),
    url(r'^presencaCreate/', PresencaCreate.as_view(), name="presencaCreate"),
    url(r'^presencaUpdate/(?P<pk>[0-9,-1]+)', PresencaUpdate.as_view(), name="presencaUpdate"),
    url(r'^presencaDelete/(?P<pk>[0-9,-1]+)', PresencaDelete.as_view(), name="presencaDelete"),


]