#encoding: utf-8
from django.shortcuts import render
from cronograma.forms import *
from campus.forms import *
from campus.models import Clases, AcompanamientoInSitus, Estudiante, Cursos, Actividad
from estudiante.models import InfoLaboral
import json
from django.shortcuts import redirect, render, render_to_response
from datetime import datetime, date, timedelta
from math import ceil
import datetime 
from campus.views import user_group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db.models import Q
from heapq import merge


def cronograma(request):
    # if this is a POST request we need to process the form data
    eventos = AcompanamientoInSitus.objects.all()
    grupo = user_group(request)

    if grupo == None:
        return redirect('home')

    if grupo == "Formador":
        username = request.user
        try:
            formador = Formador.objects.get(usuario=username.id)
        except Formador.DoesNotExist:
            formador = None 

        if formador == None:
            print "El formador no existe"
            return redirect('home')
        else:

            try:
                #curso = get_object_or_404(Cursos, Q(formador1=formador.id) | Q(formador2=formador.id))
                curso = Cursos.objects.filter(Q(formador1=formador.id) | Q(formador2=formador.id))
                #eventos = AcompanamientoInSitus.objects.filter(curso=curso)

            except Cursos.DoesNotExist:
                curso = None
            
            if curso == None:
                print "El formador no está asociado a ningun curso de acompanamiento"
                mensaje = "/?x=1"
                return redirect('..%s' %mensaje)

            else:
                #eventos = AcompanamientoInSitus.objects.filter(curso=curso)
                eventos = []
                for i in curso:
                    x = AcompanamientoInSitus.objects.filter(curso=i)
                    for i in range(0,len(x)):
                        eventos.append(x[i])

    if grupo == "Coordinador":
        if request.method == 'GET' and 'sede' in request.GET:
            sede = request.GET.get('sede')
            
            if sede != None:
                eventos = []                
                try:
                    curso = Cursos.objects.filter(institucion=sede)
                    for c in curso:
                        x = AcompanamientoInSitus.objects.filter(curso = c)
                    #eventos.append(x)
                        eventos = list(merge(eventos, x))
                except Exception, e:
                    eventos = []          

        else:
            eventos = AcompanamientoInSitus.objects.all()

    if request.method == 'POST':
        form2 = FiltroCronograma(request.POST)
        form = EventosAcompanamientoForm(request.POST)
                
        if form.is_valid():
            objeto = AcompanamientoInSitus()
            objeto = form.save(commit=False)
            

            postFormatoDict = request.POST.dict() #obtuvimos el post
            post = str(postFormatoDict)

            repetir_hasta = datetime.datetime.now()

            contador = 1
            repetirfecha = request.POST['repetirfecha']                
            if 'repetir-'in post and repetirfecha != "":

                global repetir_hasta
                repetir_fecha = request.POST['repetirfecha']
                repetir_fecha = str(repetir_fecha)
                repetir_hasta = datetime.datetime(int(repetir_fecha[0:4]),int(repetir_fecha[5:7]),int(repetir_fecha[8:10]))

                repetir = request.POST['repetir-']
                fecha = objeto.fecha_inicio
                #fecha = fecha.toordinal()

                mes = int(fecha.month)
                dia = int(fecha.day)
                ano = int(fecha.year)
                global contador
                if repetir == "1":
                    for i in range(1, int((repetir_hasta - fecha).days + 2)):
                        if ((dia + 1) > 31) and (mes == 1):
                            global mes, dia, ano
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                           
                        elif ((dia + 1) > 31) and (mes == 12):
                            global mes, dia, ano
                            #global dia
                            dia = (dia + 1) - 31
                            mes = (mes + 1) -12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 3):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 5):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 7):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 8):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 10):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 4):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 6):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 9):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 11):
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 28) and (mes == 2): 
                            global mes, dia
                            #global dia
                            dia = (dia + 1) - 28
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        else:
                            global dia
                            dia = dia + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = AcompanamientoInSitus()
                        objetoi.curso=objeto.curso
                        
                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        
                        objetoi.save() 
                        SoporteAcompanamiento.objects.create(acompanamiento=objetoi)

                                                   

                if repetir == "2":
                    global mes, dia, ano
                    for i in range(1, (int((repetir_hasta - fecha).days + 2)/7)+1):
                        if ((dia + 7) > 31) and (mes == 1):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                           
                        elif ((dia + 7) > 31) and (mes == 12):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = (mes + 1) - 12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 3):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 5):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 7):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 8):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 10):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 4):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 6):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 9):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 11):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 28) and (mes == 2): 
                            #global dia
                            dia = (dia + 7) - 28
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        else:
                            dia = dia + 7
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = AcompanamientoInSitus()
                        objetoi.curso=objeto.curso

                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        
                        objetoi.save()
                        SoporteAcompanamiento.objects.create(acompanamiento=objetoi)
                
                if repetir == "3":

                    meses_entre_anos = 0

                    if((int(repetir_hasta.year)-int(fecha.year))>0):
                        meses_entre_anos = ((int(repetir_hasta.year)-int(fecha.year))*12)
                    
                    else:
                        meses_entre_anos=0


                    numero_meses = ((12 - int(fecha.month))+meses_entre_anos) - (12 - int(repetir_hasta.month)) + 1

                    global numero_meses

                    for i in range(1, numero_meses ):
                        global mes, ano
                        if mes == 12:
                            mes = (mes + 1)-12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                           
                        else:
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = AcompanamientoInSitus()
                        objetoi.curso=objeto.curso

                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        
                        objetoi.save()
                        SoporteAcompanamiento.objects.create(acompanamiento=objetoi)


            
            objeto.nombre=(objeto.nombre)+" 1"
            #objeto.tipo = "2"
            objeto.save()
            SoporteAcompanamiento.objects.create(acompanamiento=objeto)


            return redirect('cronograma_acompanamiento')
    else:

        form = EventosAcompanamientoForm(initial={'nombre': 'Visita'})
        form2 = FiltroCronograma()


    

    events = []

    for i in eventos:
        inicio = i.fecha_inicio
        #fin = i.fecha_finalizacion

        hora_inicio = [i.fecha_inicio.hour, i.fecha_inicio.minute, 0]
        #hora_finalizacion = [i.fecha_finalizacion.hour, i.fecha_finalizacion.minute, 0]
        hora_finalizacion = [i.fecha_inicio.hour + i.duracion, i.fecha_inicio.minute, 0]

        diasTotal = 0
        
        #diasEvento = 1
        diasEvento = []
        for j in range(0, diasTotal+1):
            aux = inicio + timedelta(days = j)
            diasEvento.append([aux.year, aux.month-1, aux.day])

        cursovar = Cursos.objects.get(id=i.curso.id)
        cursos = str(cursovar.descripcion)

        #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+cursos

        events.append({
            'id': i.id,
            'nombre': i.nombre,
            'curso': cursos,
            #'institucion': i.institucion,
            'descripcion': cursos,
            'hora_inicio': hora_inicio,
            'hora_finalizacion': hora_finalizacion,
            'diasEvento': diasEvento,
            
        })
    '''
    for i in eventos:
        inicio = i.fecha_inicio
        fin = i.fecha_finalizacion
        events.append({
            'nombre': i.nombre,
            'inicio': [inicio.year, inicio.month-1, inicio.day],
            'fin': [fin.year, fin.month-1, fin.day],
            'descripcion': i.descripcion
        })'''
    
    return render(request, 'cronograma.html', {
        'formAcompanamiento': form,

        'eventos': json.dumps(events),
        'user_group': user_group(request),
        'opcion_menu': 4,
        'form2':form2,
    })


def menor10(val):
    if val < 100:
        if val < 10:
            return "00"+str(val)
        else:
            return "0"+str(val)
    return str(val)

def diplomado(request):
    # if this is a POST request we need to process the form data
    eventos = Clases.objects.all()
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    if grupo == "Formador":
        username = request.user
        try:
            formador = Formador.objects.get(usuario=username.id)
            #formador = get_object_or_404(Formador, usuario=username.id)
        except Formador.DoesNotExist:
            formador = None 

        if formador == None:
            print "El formador no existe"
            return redirect('home')
        else:

            try:
                curso = Cursos.objects.filter(Q(formador1=formador.id) | Q(formador2=formador.id))
               
            except Cursos.DoesNotExist:
                curso = None
            
            if curso == None:
                print "El formador no está asociado a ningun curso de diplomado"
                mensaje = "/?x=1"
                return redirect('..%s' %mensaje)
            
            else:
                eventos = []
                for i in curso:
                    x = Clases.objects.filter(curso=i)
                    for i in range(0,len(x)):
                        eventos.append(x[i])
    elif grupo == "Coordinador":
        #if request.method == 'GET' and 'sede' in request.GET and 'grupo' in request.GET:
        if request.GET and 'grupo' in request.GET:
            #sede = request.GET.get('sede')
            grupo = request.GET.get('grupo')
            
            eventos = []

            if grupo == '0':
                #curso = Cursos.objects.filter(institucion=sede)
                curso = Cursos.objects.all()
            else:
                #curso = Cursos.objects.filter(institucion=sede, id=grupo)
                curso = Cursos.objects.filter(id=grupo)

            for c in curso:
                x = Clases.objects.filter(curso = c)
                eventos = list(merge(eventos, x))
        else:
            eventos = Clases.objects.all()

    if request.method == 'POST':
        form2 = FiltroCronograma(request.POST)
        form = EventosDiplomadoForm(request.POST)
        if form.is_valid():
            objeto = Clases()

            
            objeto = form.save(commit=False)
           

            postFormatoDict = request.POST.dict() #obtuvimos el post
            post = str(postFormatoDict)

            repetir_hasta = datetime.datetime.now()

            contador = 1 
            repetirfecha = request.POST['repetirfecha']                
            if 'repetir-'in post and repetirfecha != "":    

                global repetir_hasta
                repetir_fecha = request.POST['repetirfecha']
                repetir_fecha = str(repetir_fecha)
                repetir_hasta = datetime.datetime(int(repetir_fecha[0:4]),int(repetir_fecha[5:7]),int(repetir_fecha[8:10]))

                repetir = request.POST['repetir-']
                fecha = objeto.fecha_inicio
                #fecha = fecha.toordinal()

                mes = int(fecha.month)
                dia = int(fecha.day)
                ano = int(fecha.year)

                                           
                if repetir == "1":
                    global mes, dia, ano
                    for i in range(1, int((repetir_hasta - fecha).days + 2)):
                        if ((dia + 1) > 31) and (mes == 1):
                            #global dia
                            dia = (dia + 1) - 31  
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                           
                        elif ((dia + 1) > 31) and (mes == 12):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = (mes + 1) -12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 3):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 5):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 7):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 8):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 31) and (mes == 10):
                            #global dia
                            dia = (dia + 1) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 4):
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 6):
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 9):
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 30) and (mes == 11):
                            #global dia
                            dia = (dia + 1) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 1) > 28) and (mes == 2): 
                            #global dia
                            dia = (dia + 1) - 28
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        else:
                            dia = dia + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = Clases()
                        objetoi.curso=objeto.curso
                        global contador
                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        #objetoi.tipo=objeto.tipo
                        objetoi.save()
                        SoporteClases.objects.create(clase=objetoi)
                                                   

                if repetir == "2":
                    global mes, dia, ano
                    for i in range(1, (int((repetir_hasta - fecha).days + 2)/7)+1):
                        if ((dia + 7) > 31) and (mes == 1):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                           
                        elif ((dia + 7) > 31) and (mes == 12):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = (mes + 1) - 12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 3):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 5):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 7):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 8):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 31) and (mes == 10):
                            #global dia
                            dia = (dia + 7) - 31
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 4):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 6):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 9):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 30) and (mes == 11):
                            #global dia
                            dia = (dia + 7) - 30
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        elif ((dia + 7) > 28) and (mes == 2): 
                            #global dia
                            dia = (dia + 7) - 28
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        else:
                            dia = dia + 7
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = Clases()
                        objetoi.curso=objeto.curso

                        global contador
                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        #objetoi.tipo=objeto.tipo
                        objetoi.save()
                        SoporteClases.objects.create(clase=objetoi)
                
                if repetir == "3":

                    meses_entre_anos = 0

                    if((int(repetir_hasta.year)-int(fecha.year))>0):

                        global meses_entre_anos
                        meses_entre_anos = (int(repetir_hasta.year)-int(fecha.year))*12
                        #print "meses entre anos "+str(meses_entre_anos)
                    
                    else:
                        global meses_entre_anos
                        #print "no hay entre anos"
                        meses_entre_anos=0


                    numero_meses = ((12 - int(fecha.month))+meses_entre_anos) - (12 - int(repetir_hasta.month)) + 1

                    global numero_meses
                    global contador
                    for i in range(1, numero_meses ):
                        global mes, ano
                        if mes == 12:
                            mes = (mes + 1)-12
                            ano = ano + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                        else:
                            mes = mes + 1
                            nueva_fecha = datetime.datetime(ano, mes, dia, fecha.hour, fecha.minute, 00, 000000)
                            
                        objetoi = Clases()
                        objetoi.curso=objeto.curso
                        contador = contador + 1
                        objetoi.nombre=str(objeto.nombre)+ " "+ str(contador)
                        objetoi.fecha_inicio=nueva_fecha
                        objetoi.duracion=objeto.duracion
                        objetoi.descripcion=objeto.descripcion
                        #objetoi.tipo=objeto.tipo
                        objetoi.save()
                        SoporteClases.objects.create(clase=objetoi)


            objeto.nombre = str(objeto.nombre) + " 1"
            #objeto.tipo = "1"
            objeto.save()
            SoporteClases.objects.create(clase=objeto)
           
            return redirect('cronograma_diplomado')
    else:
        form = EventosDiplomadoForm(initial={'nombre': 'Sesion'}) 
        form2 = FiltroCronograma()

    #eventos = Clases.objects.all()
    #
    events = []
    for i in eventos:
        inicio = i.fecha_inicio
        #fin = i.fecha_finalizacion

        hora_inicio = [i.fecha_inicio.hour, i.fecha_inicio.minute, 0]
        #hora_finalizacion = [i.fecha_finalizacion.hour, i.fecha_finalizacion.minute, 0]
        hora_finalizacion = [i.fecha_inicio.hour + i.duracion, i.fecha_inicio.minute, 0]

        diasTotal = 0
        
        #diasEvento = 1
        diasEvento = []
        for j in range(0, diasTotal+1):
            aux = inicio + timedelta(days = j)
            diasEvento.append([aux.year, aux.month-1, aux.day])

        cursovar = Cursos.objects.get(id=i.curso.id)
        cursos = str(cursovar.descripcion)
        cohorte = i.curso.cohorte
        

        events.append({
            'id': i.id,
            'nombre': i.nombre,
            #'curso': i.curso,
            #'institucion': i.institucion,
            'descripcion': cursos,
            'hora_inicio': hora_inicio,
            'hora_finalizacion': hora_finalizacion,
            'diasEvento': diasEvento,
            'cohorte': " (Cohorte "+str(cohorte)+")",
        })
    
    return render(request, 'diplomado.html', {
        'formDiplomado': form,
        'eventos': json.dumps(events),
        'user_group': user_group(request),
        'opcion_menu': 3,
        'form2':form2,
    })

def filtro_diplomado(request):
    if request.method == 'POST':
        form = FiltroCronograma(request.POST)
        if form.is_valid():
            #sede = form.cleaned_data['sedes']
            grupo = form.cleaned_data['grupos']

            response = redirect('cronograma_diplomado')
            #response['Location'] += "?sede="+sede+'&grupo='+grupo
            response['Location'] += "?grupo="+grupo
            return response
        else:
            return redirect('cronograma_diplomado')    
    else:
        return redirect('cronograma_diplomado')

def filtro_acompanamiento(request):
    if request.method == 'POST':
        form = FiltroCronograma(request.POST)
        if form.is_valid():
            sede = form.cleaned_data['sedes']
            grupo = form.cleaned_data['grupos']

            response = redirect('cronograma_acompanamiento')
            response['Location'] += "?sede="+sede+'&grupo='+grupo
            return response
        else:
            return redirect('cronograma_acompanamiento')    
    else:
        return redirect('cronograma_acompanamiento')

def diplomado_modificar(request):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    idCurso = request.GET.get('idCurso')
    curso = Clases.objects.filter(id=idCurso)[0]
    try:
        url = SoporteClases.objects.get(clase = curso)
    except:
        url = "#"

    urlboolean = True
    if url.archivo == "":
        urlboolean = False
    
    if request.method == 'POST':

        get = request.POST['boton']
        
        if get == "0":

            form = EventosDiplomadoMForm(request.POST, instance=curso)
            if form.is_valid():
                objeto = form.save()
                objeto.save()
                return redirect('cronograma_diplomado')

        if get == "1":
            form = EventosDiplomadoMForm(instance=curso)

        if get == "2":
            idCurso = request.GET.get('idCurso')
            curso = Clases.objects.filter(id=idCurso)[0]
            curso.delete()
            return redirect('cronograma_diplomado')
    else:
        form = EventosDiplomadoMForm(instance=curso)

    var = curso.id

    return render(request, 'diplomado_modificar.html', {
        'form': form, 
        'user_group': user_group(request),
        'opcion_menu': 3, 'curso': var, 'url':url.archivo, 'urlboolean':urlboolean
    })

def acompanamiento_modificar(request):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    idCurso = request.GET.get('idCurso')
    curso = AcompanamientoInSitus.objects.filter(id=idCurso)[0]

    
    url = SoporteAcompanamiento.objects.get(acompanamiento = curso)
    

    if request.method == 'POST':

        get = request.POST['boton']
        
        if get == "0":

            form = EventosAcompanamientoMForm(request.POST, instance=curso)
            if form.is_valid():
                objeto = form.save()
                objeto.save()
                return redirect('cronograma_acompanamiento')

        if get == "1":
            form = EventosAcompanamientoMForm(instance=curso)

        if get == "2":
            idCurso = request.GET.get('idCurso')
            curso = AcompanamientoInSitus.objects.filter(id=idCurso)[0]
            curso.delete()
            return redirect('cronograma_acompanamiento')
    else:
        form = EventosAcompanamientoMForm(instance=curso)

    return render(request, 'acompanamiento_modificar.html', {
        'form': form, 
        'user_group': user_group(request),
        'opcion_menu': 4,
        'curso':idCurso,
        'url':url.archivo,
    
    })

def subirsoportes(request):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    identificador = request.GET['v']
    clase = Clases.objects.get(id=identificador)
    curso = clase.curso
    soporteclases = SoporteClases.objects.get(clase=clase.id)

    if request.method == 'POST':
        
        form = DocumentosSoporteForm(request.POST, request.FILES, instance=soporteclases)
        
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.clase = Clases.objects.get(clase=clase.id)
            obj.save()
            #soporte.clase = clase
            #soporteclases.archivo = obj.archivo
            #soporteclases.save()
            
            ide = "?v="+str(clase.id)

            form = DocumentosSoporteForm(instance=soporteclases)

            x = "?v="+str(clase.id)

            return HttpResponseRedirect('cronograma_diplomado_soportes%s' %x)
            '''
            return render(request, 'diplomado_soportes.html', {
            'form': form,
            'user_group': user_group(request),
            'opcion_menu': 3,
            'clase' : clase.id,
            'curso' : curso.id,
            'x':1,
        })'''
    else:   

        form = DocumentosSoporteForm(instance=soporteclases)
        
    return render(request, 'diplomado_soportes.html', {
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 3,
        'clase' : clase.id,
        'curso' : curso.id,
    })

def subirsoportesacompanamiento(request):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    identificador = request.GET['v']
    acompanamiento= AcompanamientoInSitus.objects.get(id=identificador)
    curso = acompanamiento.curso
    soporteclases = SoporteAcompanamiento.objects.get(acompanamiento=acompanamiento.id)

    if request.method == 'POST':
       
        form = DocumentosSoporteAcompanamientoForm(request.POST, request.FILES, instance=soporteclases)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.acompanamiento = acompanamiento
            obj.save()

            form = DocumentosSoporteAcompanamientoForm(instance=soporteclases)

            x = "?v="+str(acompanamiento.id)

            return HttpResponseRedirect('cronograma_acompanamiento_soportes%s' %x)
            
            '''
            return render(request, 'cronograma_soportes.html', {
                'form': form,
                'user_group': user_group(request),
                'opcion_menu': 4,
                'clase' : acompanamiento.id,
                'curso' : curso.id,
                'x':1,
            })
            '''

    else:
        
        form = DocumentosSoporteAcompanamientoForm(instance=soporteclases)

        
    return render(request, 'cronograma_soportes.html', {
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 4,
        'clase' : acompanamiento.id,
        'curso' : curso.id,
    })

def prev_add_curso(request):

    grupo = user_group(request)
    est = Estudiante.objects.all()
    infos = InfoLaboral.objects.filter(estudiante__in=est)

    if grupo == None:
        return redirect('home')

    if request.method == 'POST':
        form = EstudiantesCurso(request.POST)
        if form.is_valid():
            jornada = form.cleaned_data['jornadas']
            sds = form.cleaned_data['sedes']
            cohorte = form.cleaned_data['cohorte']
            sedes = "?sedes="
            for sede in sds:
                sedes+=sede+","
            sedes = sedes[:-1]
            response = redirect('add_curso')
            response['Location'] += sedes+'&jornada='+jornada+'&cohorte='+cohorte
            return response
            #return redirect('gestion_cursos', sede, jornada)
    else :
        form = EstudiantesCurso()

    return render(request, 'prev_curso.html', {
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
        'infos': infos
    })

def curso(request):

    sedes = request.GET.get('sedes')
    jornada = request.GET.get('jornada')
    cohorte = request.GET.get('cohorte')
    sede = sedes.split(',');

    if not sede or not jornada:
        return redirect('prev_add_curso')

    grupo = user_group(request)
    est = Estudiante.objects.all()
    infos = InfoLaboral.objects.filter(estudiante__in=est)

    if grupo == None:
        return redirect('home')

    if request.method == 'POST':
        form = CursoForm(request.POST, sede=sede, jornada=jornada, cohorte=cohorte)
        if form.is_valid():
            objeto = form.save(commit=False)
            if cohorte == '3':
                objeto.cohorte = 3
            elif cohorte == '4':
                objeto.cohorte = 4
            else:
                objeto.cohorte = 2
            objeto.save()
            form.save_m2m()
            
            '''response = redirect('add_curso')
            response['Location'] +="?sedes="+ sedes+'&jornada='+jornada
            return response'''
            return redirect('gestion_cursos')
    else :
        form = CursoForm(sede=sede, jornada=jornada, cohorte=cohorte)

    ids_estudiantes = InfoLaboral.objects.filter(sede__in=sede, jornada=jornada).values('estudiante')
    estudiantes = []
    for i in ids_estudiantes:
        est = Estudiante.objects.get(id=i['estudiante'])
        estudiantes.append({'cc':est.numero_documento, 'nombre':est.nombre_completo()})

    return render(request, 'curso.html', {
        'form': form,
        'cohorte': cohorte,
        'user_group': user_group(request),
        'opcion_menu': 5,
        'infos': infos,
        'estudiantes': json.dumps(estudiantes)
    })

def formador(request):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    if request.method == 'POST':
        form = FormadorForm(request.POST)
        if form.is_valid():
            objeto = form.save(commit=False)
            objeto.cohorte = 2
            formador = Formador.objects.filter(usuario=objeto.usuario)
            if not formador:
                objeto.save()
            else:
                form = FormadorForm(request.POST)
                return render(request, 'formador.html', {
                    'form': form,
                    'user_group': user_group(request),
                    'opcion_menu': 5,
                })
            
            return redirect('gestion_formador')
    else :
        form = FormadorForm()

    return render(request, 'formador.html', {
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
    })

def reporte_cursos(request, limit=100):

    curso_list = Cursos.objects.all() 
    
    for i in curso_list:
        descripcion = i.descripcion.split(" ")
        #numero_curso = i.descripcion[6:]
        #numero_curso = menor10(int(numero_curso))
        i.descripcion = descripcion[0]+" "+menor10(int(descripcion[1])) #i.descripcion[:6]+numero_curso
        i.save()

    curso_list = Cursos.objects.all().order_by('descripcion') 
    
    #estudiante_list = [curso_list.lenght]
    #estudiante_list = curso_list[0].estudiantes.all()
    #estudiante_list = [curso_list.lenght]
    #for i in range(0, curso_list.lenght - 1 ):
    #    estudiante_list[i] = curso_list[i].estudiantes.all()
             
    
    return render(request, 'gestion.html', {'curso_list': curso_list,  'user_group': user_group(request),
        'opcion_menu': 5, },
        )

def reporte_formadores(request, limit=100):
    formador_list = Formador.objects.all() 
    #estudiante_list = [curso_list.lenght]
    #estudiante_list = curso_list[0].estudiantes.all()
    #estudiante_list = [curso_list.lenght]
    #for i in range(0, curso_list.lenght - 1 ):
    #    estudiante_list[i] = curso_list[i].estudiantes.all()
             
    
    return render(request, 'gestion_formador.html', {'formador_list': formador_list,  'user_group': user_group(request),
        'opcion_menu': 5, },
        )
    
def lista_estudiantes(request, id):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    clase = Clases.objects.get(id=id)
    curso = clase.curso
    clasenombre = clase.nombre
    cursonombre = curso.descripcion
    clasefecha = clase.fecha_inicio

    formador1 = curso.formador1
    formador2 = curso.formador2
    institucion = curso.institucion

    estudiante_list = curso.estudiantes.all()
    
    
    return render(request, 'lista_estudiantes.html', {'estudiante_list': estudiante_list,  'user_group': user_group(request),
        'opcion_menu': 5, 'curso':cursonombre, 'clase':clasenombre, 'clase_fecha':clasefecha, 
        'formador1':formador1,'formador2':formador2, 'institucion':institucion, 'cursoTotal': curso},
        )

def lista_acompanamiento(request, id):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    clase = AcompanamientoInSitus.objects.get(id=id)
    curso = clase.curso
    clasenombre = clase.nombre
    cursonombre = curso.descripcion
    estudiante_list = curso.estudiantes.all()
    clasefecha = clase.fecha_inicio

    formador1 = curso.formador1
    formador2 = curso.formador2
    institucion = curso.institucion
    
    
    return render(request, 'lista_estudiantes.html', {'estudiante_list': estudiante_list,  'user_group': user_group(request),
        'opcion_menu': 5, 'curso':cursonombre, 'institucion':institucion, 'clase':clasenombre, 'clase_fecha':clasefecha,
        'formador1':formador1,'formador2':formador2, },
        )

def detalle_curso(request, id):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    curso = Cursos.objects.get(id=id)
    #clase = Clases.objects.filter(curso=curso.id)


    if request.method == 'POST':

        get = request.POST['boton']
        #print "!!!!!!!!!!!!!!!!"+str(get)
        
        if get == "0":
            form = CursoMForm(request.POST, instance=curso, cohorte=curso.cohorte)
            if form.is_valid():
                objeto = form.save()
                '''
                formador = Cursos.objects.all().exclude(id = curso.id)
                for i in formador:
                    if objeto.formador1 == i.formador1 or objeto.formador2 == i.formador1 or objeto.formador2 == i.formador1 or objeto.formador2 == i.formador2 :
                        form = CursoMForm(instance=curso)
                        return render(request, 'detalles_curso.html', {
                            'form': form, 
                            'user_group': user_group(request),
                            'x': 1,
                        })
                '''
                objeto.save()

                return redirect('gestion_cursos')

        if get == "2":
            form = CursoMForm(instance=curso, cohorte=curso.cohorte)

        if get == "1":
            curso = Cursos.objects.get(id=id)
            curso.delete()
            return redirect('gestion_cursos')
    else:
        form = CursoMForm(instance=curso, cohorte=curso.cohorte)
    
    return render(request, 'detalles_curso.html', {
        'form': form, 
        'user_group': user_group(request),
        'opcion_menu': 5,
        'curso':curso.id,
        'cohorte': curso.cohorte,
    })

def reporte_conformacion_curso(request, id):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    #clase = Clases.objects.get(id=id)
    curso = Cursos.objects.get(id=id)
    #clasenombre = clase.nombre
    cursonombre = curso.descripcion
    #clasefecha = clase.fecha_inicio

    formador1 = curso.formador1
    formador2 = curso.formador2
    institucion = curso.institucion

    estudiante_list = curso.estudiantes.all()
    count =0
    
    return render(request, 'lista_estudiantes.html', {
        'estudiante_list': estudiante_list,
        'user_group': user_group(request),
        'opcion_menu': 5,
        'curso':cursonombre,
        'formador1':formador1,
        'formador2':formador2,
        'institucion':institucion,
        'cursoTotal':curso,
        })

def detalle_formador(request, id):

    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    curso = Formador.objects.get(id=id)


    if request.method == 'POST':

        get = request.POST['boton']
        
        
        if get == "0":

            form = FormadorModificacionForm(request.POST, instance=curso)
            if form.is_valid():
                objeto = form.save()
                objeto.save()
                return redirect('gestion_formador')

        if get == "2":
            form = FormadorModificacionForm(instance=curso)

        if get == "1":
            formador = Formador.objects.get(id=id)
            print "!!!!!!!!!!!!!!!!!!"+str(formador.nombre1)
            formador.delete()
            return redirect('gestion_cursos')
    else:
        form = FormadorModificacionForm(instance=curso)

    return render(request, 'detalles_formador.html', {
        'form': form, 
        'user_group': user_group(request),
        'opcion_menu': 4,
    })

def actividad(request, id):
    #
    clase = get_object_or_404(Clases, id=id)
    print "--------"
    curso = clase.curso
    actividades = Actividad.objects.filter(clase=clase)
    estudiante_list = curso.estudiantes.all()

    grupo = user_group(request)
    if grupo == None:
        return redirect('cronograma_diplomado_soportes')

    if request.method == 'POST':
        
        form = ActividadForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.clase = clase
            obj.save()
            obj.estudiantes = curso.estudiantes.all()
            obj.save()
            
            return redirect('actividad', id)
        else:
            print "aaaaaasss"

    else:        
        form = ActividadForm()

    return render(request, 'actividadesyasistencia.html', {
        'clase':clase.id,
        'id': id,
        'curso': curso.id,
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
        'estudiante_list':estudiante_list,
        'actividades': actividades
    })

def asistenciaClases(request, idC, idA):
    clase = get_object_or_404(Clases, id=idC)
    actividad = Actividad.objects.get(id=idA)
    idCurso = clase.curso

    if request.method == 'POST':
        form = ActividadAsistenciaForm(request.POST, instance=actividad, idCurso=idCurso)
        if form.is_valid():
            obj = form.save()
            return redirect('actividad', idC)

    else:        
        form = ActividadAsistenciaForm(idCurso=idCurso, instance=actividad)

    return render(request, 'asistenciaClases.html', {
        'clase':clase.id,
        'form': form,
        'idC': idC,
         'user_group': user_group(request),
         'actividad': actividad
    })

def asistenciaClases2(request, idC, idA):
    clase = get_object_or_404(AcompanamientoInSitus, id=idC)
    actividad = Actividad.objects.get(id=idA)
    idCurso = clase.curso

    if request.method == 'POST':
        form = ActividadAsistenciaAcompanamientoForm(request.POST, instance=actividad, idCurso=idCurso)
        if form.is_valid():
            obj = form.save()
            return redirect('actividad_acompanamiento', idC)

    else:        
        form = ActividadAsistenciaAcompanamientoForm(idCurso=idCurso, instance=actividad)

    return render(request, 'asistenciaclases2.html', {
        'clase':clase.id,
        'form': form,
        'idC': idC,
        'user_group': user_group(request),
    })

def actividadacompanamiento(request, id):
    clase = get_object_or_404(AcompanamientoInSitus, id=id)
    print "--------"
    curso = clase.curso
    actividades = ActividadAcompanamiento.objects.filter(clase=clase)
    estudiante_list = curso.estudiantes.all()

    grupo = user_group(request)
    if grupo == None:
        return redirect('cronograma_diplomado_soportes')

    if request.method == 'POST':
        
        form = ActividadAcompanamientoForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.clase = clase
            obj.save()
            obj.estudiantes = curso.estudiantes.all()
            obj.save()
            
            return redirect('actividad_acompanamiento', id)
        else:
            print "aaaaaasss"

    else:        
        form = ActividadAcompanamientoForm()

    return render(request, 'actividadacompanamiento.html', {
        'clase':clase.id,
        'id': id,
        'curso': curso.id,
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
        'estudiante_list':estudiante_list,
        'actividades': actividades})

def cancelar_clase_acompanamiento(request, id):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    postFormatoDict = request.POST.dict() #obtuvimos el post
    post = str(postFormatoDict)
    clase = AcompanamientoInSitus.objects.get(id=id)
    motivos = ""
    if "motivos" in post:
        motivos = request.POST['motivos']
                   
        
        clase.nombre = "CANCELADA "+clase.nombre
        clase.descripcion = motivos + clase.descripcion
        clase.estado = False
        clase.save()
        return redirect('cronograma_acompanamiento')
    
    return render(request, 'cancelarvisita.html', {'user_group': user_group(request),
        'opcion_menu': 5,'var':clase.id,},
        )

def cancelar_clase_diplomado(request, id):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    postFormatoDict = request.POST.dict() #obtuvimos el post
    post = str(postFormatoDict)
    clase = Clases.objects.get(id=id)
    motivos = ""
    if "motivos" in post:
        motivos = request.POST['motivos'] 
        clase.nombre = "CANCELADA "+clase.nombre
        clase.descripcion = motivos 
        clase.estado = False
        clase.save()
        return redirect('cronograma_diplomado')
    
    return render(request, 'cancelarsesion.html', {'user_group': user_group(request),
        'opcion_menu': 5,'var':clase.id,},
        )

def gestion(request):
    grupo = user_group(request)
    if grupo == None:
        return redirect('home')

    curso_list = Cursos.objects.all()
    formador_list = Formador.objects.all()
    
    return render(request, 'contenidogestion.html', {'user_group': user_group(request),
        'opcion_menu': 5, 'curso_list':curso_list, 'formador_list': formador_list,},
        )

def asistencia(request, curso_id, clase_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    clase = get_object_or_404(Clases, id=clase_id)

    if request.method=='POST':
        form = AsistenciaForm(request.POST, instance=clase)
        #soportesFormset = SoportesFormset(request.POST, request.FILES, instance=clase)
        #advertencia: no trate de copiar este codigo, trabaja de manera inusual
        if form.is_valid() : 
            form.save()
        #if soportesFormset.is_valid() : 
            #result = soportesFormset.save()
            #print "result=",result
        
        #print "valido1=", form.is_valid(), "valido2=", soportesFormset.is_valid()

        #if form.is_valid() and soportesFormset.is_valid():
            #return redirect('asistencia', curso_id, clase_id)

            ide = "?v="+str(clase_id)

            return HttpResponseRedirect('../../../cronograma_diplomado_soportes%s' %ide)


    else :
        form = AsistenciaForm(instance=clase)
        #soportesFormset = SoportesFormset(instance=clase)

    return render(request, 'asistencia.html', {
        'clase':clase,
        'curso': curso,
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
        #'soportesFormset' : soportesFormset,
    })

def asistencia_acompanamiento(request, curso_id, clase_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    clase = get_object_or_404(AcompanamientoInSitus, id=clase_id)

    if request.method=='POST':
        form = AsistenciaForm(request.POST, instance=clase)
        #soportesFormset = SoportesFormset(request.POST, request.FILES, instance=clase)
        #advertencia: no trate de copiar este codigo, trabaja de manera inusual
        if form.is_valid() : 
            form.save()
        #if soportesFormset.is_valid() : 
            #result = soportesFormset.save()
            #print "result=",result
        
        #print "valido1=", form.is_valid(), "valido2=", soportesFormset.is_valid()

        #if form.is_valid() and soportesFormset.is_valid():
            #return redirect('asistencia', curso_id, clase_id)

            ide = "?v="+str(clase_id)

            return HttpResponseRedirect('../../../cronograma_acompanamiento_soportes%s' %ide)


    else :
        form = AsistenciaForm(instance=clase)
        #soportesFormset = SoportesFormset(instance=clase)

    return render(request, 'asistencia_acompanamiento.html', {
        'clase':clase,
        'curso': curso,
        'form': form,
        'user_group': user_group(request),
        'opcion_menu': 5,
        #'soportesFormset' : soportesFormset,
    })

