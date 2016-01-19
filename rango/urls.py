from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/',views.about, name='about'),
    url(r'^bar/(?P<nombre_bar>[\w\-]+)/$',views.bar, name='bar'),
    url(r'^registrar/',views.registro, name='registro'),
    url(r'^salir/',views.salir, name='salir'),
    url(r'^entrar/',views.entrar, name='entrar'),
    url(r'^add_tapa/',views.add_tapa, name='add_tapa'),
    url(r'^reclamar_datos/',views.reclamar_datos, name='reclamar_datos'),
    url(r'^me_gusta/',views.me_gusta, name='me_gusta'),
                       )