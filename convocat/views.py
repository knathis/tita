from django.shortcuts import render

# Create your views here.

# vistas de la parte PUBLICA
def index(request):
    return render(request, 'publico/index.html', {
        'opcion_menu': 1
    })

def objetivos(request):
    return render(request, 'publico/objetivos.html', {
        'opcion_menu': 2
    })

def funciones(request):
    return render(request, 'publico/funciones.html', {
        'opcion_menu': 3
    })

def requisitos(request):
    return render(request, 'publico/requisitos.html', {
        'opcion_menu': 4
    })

# falta por hacer
def registrarse(request):
    return render(request, 'publico/registrarse.html', {
        'opcion_menu': 5
    })
def formulario(request):
    return render(request, 'publico/formulario_aspirante.html', {
        'opcion_menu': 6
    })

# fin vistas de la parte PUBLICA