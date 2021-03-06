from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('campus.views',
    url(r'cursos$',      'listar_cursos_profesor', name="listar_cursos_profesor"),
    url(r'calificacion/clases/(\d+)$',      'listar_clases_curso', name="listar_clases_curso"),
    url(r'cursos/(\d+)/clases/(\d+)/asistencia$',       'asistencia', name="asistencia"),
    url(r'cursos/(\d+)/clases/(\d+)/actividades$',      'calificar_actividades', name="calificar_actividades"),
)