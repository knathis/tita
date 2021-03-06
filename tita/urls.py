from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # solo en servidor de desarrollo


urlpatterns += patterns('',
    url(r'^select2/', include('django_select2.urls')),

    url(r'^logged_user$', 'campus.views.logged_user', name="logged_user"),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'home'}, name='logout'),
    url(r'^cambiar-pass/$', 'django.contrib.auth.views.password_change', {'template_name':'cambiar-pass.html', 'post_change_redirect':'home'}, name='cambiar_pass'),

    url(r'^admin/', include(admin.site.urls)),

    #url(r'^$', TemplateView.as_view(template_name='info/index.html'), name='home'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^antecedentes/$', TemplateView.as_view(template_name='info/antecedentes.html'), name="info_antecedentes"),
    url(r'^infogeneral/$', TemplateView.as_view(template_name='info/infogeneral.html'), name="info_general"),
    url(r'^calendario/$', TemplateView.as_view(template_name='info/calendario.html'), name="info_calendario"),
    url(r'^requisitos/$',TemplateView.as_view(template_name='info/requisitos.html'), name="info_requisitos"),
    url(r'^registrarse/$',TemplateView.as_view(template_name='info/registrarse.html'), name="info_registrarse"),
    url(r'^contactenos/$',TemplateView.as_view(template_name='info/contactenos.html'), name="info_contactenos"),
    #url(r'^tablero_control/$',TemplateView.as_view(template_name='dashboard/tablero_control.html'), name="tablero_control"),


    url('', include('convocat.urls')),
    url('', include('convocat2.urls')),
    url('', include('estudiante.urls')),
    url(r'^encuestas/', include('survey.urls')),
    url(r'^campus/', include('campus.urls')),
    url('', include('cronograma.urls')),
    url('', include('malla.urls')),
    url('', include('bilinguismo.urls')),
)