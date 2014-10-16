# encoding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
#import settings

from models import Question, Survey, Category
from forms import ResponseForm




def encuesta_padre(request):
    survey = Survey.objects.get(id=1)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            form.save()
            return redirect('encuesta_finalizada')
        else:
            print "error llenando", form.errors
    else :
        form = ResponseForm(survey=survey)

    # customizar form de acuerdo a la encuesta para padres
    #form.fields['jornada'].label = u"1. Jornada en la que estudia su hijo(a)"
    #form.fields['nombre'].label = u"3. Nombre(s) y apellidos del padre de familia o acudiente"
    #form.fields['institucion'].label = u"5. Nombre de la institución educativa en la que estudia su hijo(a)"

    camposMaterias = [form['question_13%02d'%x] for x in xrange(1,20) ]
    camposDispositivos = [form['question_%d'%x] for x in xrange(23,27) ]
    camposUsos = [form['question_29%02d'%x] for x in xrange(1,20)]
    camposHerramientas = [form['question_19%02d'%x] for x in xrange(1,15) ]

    return render(request, 'encuesta_padre.html', {
        'form': form,
        
        'camposMaterias1': camposMaterias[:10],
        'camposMaterias2': camposMaterias[10:],
        'camposDispositivos1': camposDispositivos[:2],
        'camposDispositivos2': camposDispositivos[2:],
        'camposHerramientas1' : camposHerramientas[:7],
        'camposHerramientas2' : camposHerramientas[7:],
        'camposUsos1' : camposUsos[:10],
        'camposUsos2' : camposUsos[10:]
    })


def encuesta_docente(request):
    survey = Survey.objects.get(id=2)
    category_items = list(survey.category_set.all())    
    
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            form.save()
            return redirect('encuesta_finalizada')
        else:
            print "error llenando", form.errors
    else :
        form = ResponseForm(survey=survey)


    # customizar form de acuerdo a la encuesta para padres
    #form.fields['jornada'].label = u"1. Jornada en la que enseñas"
    #form.fields['institucion'].label = u"2. Nombre de tu institución educativa"
    #form.fields['nombre'].label = u"3. Nombre y apellidos"


    camposMaterias = [form['question_09%02d'%x] for x in xrange(1,20) ]
    camposHerramientas = [form['question_15%02d'%x] for x in xrange(1,30) ]
    camposDispositivos = [form['question_%02d'%x] for x in xrange(25,29) ]
    camposUsos = [form['question_31%02d'%x] for x in xrange(1,21) ]

    return render(request, 'encuesta_docente.html', {
        'form': form,
        'camposMaterias1': camposMaterias[:10],
        'camposMaterias2': camposMaterias[10:],
        'camposHerramientas1': camposHerramientas[:14],
        'camposHerramientas2': camposHerramientas[14:],
        'camposDispositivos1': camposDispositivos[:2],
        'camposDispositivos2': camposDispositivos[2:],
        'camposUsos1': camposUsos[:10],
        'camposUsos2': camposUsos[10:]
    })

def encuesta_estudiante(request):
    survey = Survey.objects.get(id=3)
    category_items = list(survey.category_set.all())    
    
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            form.save()
            return redirect('encuesta_finalizada')
        else:
            print "error llenando", form.errors
    else :
        form = ResponseForm(survey=survey)

    # customizar form de acuerdo a la encuesta para padres

    camposMaterias = [form['question_13%02d'%x] for x in xrange(1,20) ]
    camposRecursos = [form['question_18%02d'%x] for x in xrange(1,8) ]
    camposDispositivos = [form['question_2%0d'%x] for x in xrange(2,6) ]
    camposInternet = [form['question_28%02d'%x] for x in xrange(1,19) ]

    return render(request, 'encuesta_estudiante.html', {
        'form': form,
        'camposMaterias1': camposMaterias[:10],
        'camposMaterias2': camposMaterias[10:],
        'camposRecursos1': camposRecursos[:4],
        'camposRecursos2': camposRecursos[4:],
        'camposDispositivos1': camposDispositivos[:2],
        'camposDispositivos2': camposDispositivos[2:],
        'camposInternet1': camposInternet[:9],
        'camposInternet2': camposInternet[9:]
    })
