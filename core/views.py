from django.shortcuts import render, redirect, get_object_or_404
from core.models import ProyectoEvaluacion, ActivoDigital, Riesgo, TratamientoRiesgo
from core.forms import ProyectoEvaluacionForm, ActivoDigitalForm, ActivoDigitalEdicionForm, RiesgoEdicionForm, RiesgoForm, ShodanBusquedaForm, TratamientoRiesgoForm
from core.services.shodan_service import crear_activos_desde_shodan, resolver_objetivo, resolver_objetivo

def dashboard(request):
    proyectos = ProyectoEvaluacion.objects.all()
    return render(request, 'core/dashboard.html', {'proyectos': proyectos})

def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoEvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProyectoEvaluacionForm()

    return render(request, 'core/crear_proyecto.html', {'form': form})

def lista_activos(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoEvaluacion, id=proyecto_id)
    activos = ActivoDigital.objects.filter(proyecto=proyecto)

    return render(request, 'core/lista_activos.html', {
        'proyecto': proyecto,
        'activos': activos
    })

    
def crear_activo(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoEvaluacion, id=proyecto_id)

    if request.method == 'POST':
        form = ActivoDigitalForm(request.POST)
        if form.is_valid():
            activo = form.save(commit=False)
            activo.proyecto = proyecto
            activo.save()
            return redirect('lista_activos', proyecto_id=proyecto.id)
    else:
        form = ActivoDigitalForm()

    return render(request, 'core/crear_activo.html', {
        'form': form,
        'proyecto': proyecto
    })

def editar_activo(request, activo_id):
    activo = get_object_or_404(ActivoDigital, id=activo_id)

    if request.method == 'POST':
        form = ActivoDigitalEdicionForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect(
                'lista_activos',
                proyecto_id=activo.proyecto.id
            )
    else:
        form = ActivoDigitalEdicionForm(instance=activo)

    return render(request, 'core/editar_activo.html', {
        'form': form,
        'activo': activo
    })

def eliminar_activo(request, activo_id):
    activo = get_object_or_404(ActivoDigital, id=activo_id)
    proyecto_id = activo.proyecto.id
    activo.delete()
    return redirect('lista_activos', proyecto_id=proyecto_id)


def importar_activos_shodan(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoEvaluacion, id=proyecto_id)

    if request.method == 'POST':
        form = ShodanBusquedaForm(request.POST)
        if form.is_valid():
            objetivo = form.cleaned_data['objetivo']
    
            ip = resolver_objetivo(objetivo)
            if not ip:
                return render(request, 'core/importar_shodan.html', {
                    'form': form,
                    'proyecto': proyecto,
                    'error': 'No se pudo resolver el dominio a una IP válida'
                })



            resultado = crear_activos_desde_shodan(ip, proyecto)

            if isinstance(resultado, dict) and 'error' in resultado:
                return render(request, 'core/importar_shodan.html', {
                    'form': form,
                    'proyecto': proyecto,
                    'error': resultado['error']
                })


            return redirect('lista_activos', proyecto_id=proyecto.id)
    else:
        form = ShodanBusquedaForm()

    return render(request, 'core/importar_shodan.html', {
        'form': form,
        'proyecto': proyecto
    })


def crear_riesgo(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoEvaluacion, id=proyecto_id)

    if request.method == 'POST':
        form = RiesgoForm(request.POST)
        if form.is_valid():
            riesgo = form.save(commit=False)

            # Validación: el activo debe pertenecer al proyecto
            if riesgo.activo.proyecto != proyecto:
                return render(request, 'core/error.html', {
                    'mensaje': 'El activo no pertenece a este proyecto'
                })

            riesgo.save()
            return redirect('lista_riesgos', proyecto_id=proyecto.id)
    else:
        form = RiesgoForm()

    return render(request, 'core/crear_riesgo.html', {
        'form': form,
        'proyecto': proyecto
    })
    
def lista_riesgos(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoEvaluacion, id=proyecto_id)

    riesgos = Riesgo.objects.filter(
        activo__proyecto=proyecto
    ).order_by('-nivel_riesgo')

    return render(request, 'core/lista_riesgos.html', {
        'proyecto': proyecto,
        'riesgos': riesgos
    })

def tratamiento_riesgo(request, riesgo_id):
    riesgo = get_object_or_404(Riesgo, id=riesgo_id)

    # Evitar doble tratamiento
    if hasattr(riesgo, 'tratamiento'):
        return redirect(
            'detalle_tratamiento',
            riesgo_id=riesgo.id
        )


    if request.method == 'POST':
        form = TratamientoRiesgoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.riesgo = riesgo
            tratamiento.save()

            # Actualizar riesgo residual
            riesgo.probabilidad_residual = form.cleaned_data['probabilidad_residual']
            riesgo.impacto_residual = form.cleaned_data['impacto_residual']
            riesgo.nivel_riesgo_residual = (
                riesgo.probabilidad_residual * riesgo.impacto_residual
            )

            # Cambiar estado
            riesgo.estado = 'En tratamiento'
            riesgo.save()

            return redirect(
                'lista_riesgos',
                proyecto_id=riesgo.activo.proyecto.id
            )
    else:
        form = TratamientoRiesgoForm()

    return render(request, 'core/tratamiento_riesgo.html', {
        'form': form,
        'riesgo': riesgo
    })

def detalle_tratamiento(request, riesgo_id):
    riesgo = get_object_or_404(Riesgo, id=riesgo_id)

    tratamiento = get_object_or_404(
        TratamientoRiesgo,
        riesgo=riesgo
    )

    return render(request, 'core/detalle_tratamiento.html', {
        'riesgo': riesgo,
        'tratamiento': tratamiento
    })

def editar_riesgo(request, riesgo_id):
    riesgo = get_object_or_404(Riesgo, id=riesgo_id)

    if request.method == 'POST':
        form = RiesgoEdicionForm(request.POST, instance=riesgo)
        if form.is_valid():
            form.save()
            return redirect(
                'detalle_tratamiento',
                riesgo_id=riesgo.id
            )
    else:
        form = RiesgoEdicionForm(instance=riesgo)

    return render(request, 'core/editar_riesgo.html', {
        'riesgo': riesgo,
        'form': form
    })

