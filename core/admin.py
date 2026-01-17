from django.contrib import admin
from .models import (
    ProyectoEvaluacion,
    ActivoDigital,
    Amenaza,
    Vulnerabilidad,
    Riesgo,
    TratamientoRiesgo
)

@admin.register(ProyectoEvaluacion)
class ProyectoEvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo_organizacion',
        'responsable',
        'fecha_creacion',
        'fecha_actualizacion'
    )
    search_fields = ('nombre', 'responsable')
    list_filter = ('tipo_organizacion',)


@admin.register(ActivoDigital)
class ActivoDigitalAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo',
        'cia_promedio',
        'nivel_criticidad',
        'fuente_osint',
        'estado',
        'fecha_identificacion'
    )
    list_filter = (
        'tipo',
        'nivel_criticidad',
        'estado',
        'fuente_osint'
    )
    search_fields = ('nombre',)
    readonly_fields = ('cia_promedio', 'fecha_identificacion')


@admin.register(Amenaza)
class AmenazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


@admin.register(Vulnerabilidad)
class VulnerabilidadAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion')
    list_filter = ('tipo',)
    search_fields = ('descripcion',)


@admin.register(Riesgo)
class RiesgoAdmin(admin.ModelAdmin):
    list_display = (
        'activo',
        'amenaza',
        'vulnerabilidad',
        'nivel_riesgo',
        'nivel_riesgo_residual',
        'nivel_prioridad',
        'estado'
    )

    list_filter = (
        'nivel_prioridad',
        'estado'
    )

    search_fields = (
        'activo__nombre',
        'amenaza__nombre'
    )

    readonly_fields = ('nivel_riesgo', 'nivel_riesgo_residual')

    fieldsets = (
        ('Relación del riesgo', {
            'fields': ('activo', 'amenaza', 'vulnerabilidad')
        }),
        ('Valoración inicial', {
            'fields': ('probabilidad', 'impacto', 'nivel_riesgo')
        }),
        ('Riesgo residual', {
            'fields': (
                'probabilidad_residual',
                'impacto_residual',
                'nivel_riesgo_residual'
            )
        }),
        ('Gestión', {
            'fields': ('nivel_prioridad', 'estado')
        }),
    )


@admin.register(TratamientoRiesgo)
class TratamientoRiesgoAdmin(admin.ModelAdmin):
    list_display = (
        'riesgo',
        'estrategia',
        'control_iso_27002',
        'responsable',
        'fecha_implementacion'
    )

    list_filter = ('estrategia',)
    search_fields = ('riesgo__activo__nombre', 'control_iso_27002')
