from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
#import settings

from models import Question, Survey, Category
from forms import ResponseForm


def Index(request):
	return render(request, 'index.html')

def SurveyDetail(request, id):
	survey = Survey.objects.get(id=id)
	category_items = Category.objects.filter(survey=survey)
	categories = [c.name for c in category_items]
	print 'categories for this survey:'
	print categories
	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
	else:
		form = ResponseForm(survey=survey)
		print form
		# TODO sort by category
	return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})

def Confirm(request, uuid):
	email = settings.support_email
	return render(request, 'confirm.html', {'uuid':uuid, "email": email})

def privacy(request):
	return render(request, 'privacy.html')


def encuesta_padre(request):
	survey = Survey.objects.get(id=1)
	category_items = list(survey.category_set.all())
	#categories = [c.name for c in category_items]
	
	form = ResponseForm(request.POST or None, survey=survey)

	#camposBasicos = ( form['question_%d'%x] for x in xrange(1,11) )
	#camposUsoInternet = ( form['question_%d'%x] for x in (11,12) )

	#camposPercepcion = ( form['question_%d'%x] for x in (13,14) )
	camposMaterias = [form['question_%d'%x] for x in xrange(10,29) ]
	camposHerramientas = [form['question_%d'%x] for x in xrange(37,52) ]
	#camposAcuerdo = (form['question_%d'%x] for x in xrange(34,39) )

	return render(request, 'encuesta_padre.html', {
		'form': form,
		#'camposBasicos':camposBasicos,
		#'camposUsoInternet': camposUsoInternet,
		#'camposPercepcion' : camposPercepcion,
		'camposMaterias1': camposMaterias[:10],
		'camposMaterias2': camposMaterias[10:],
		'camposHerramientas' : camposHerramientas,
		#'camposAcuerdo': camposAcuerdo,
		#'survey': survey,
		#'categories': categories
	})
