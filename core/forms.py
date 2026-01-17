from django import forms
from .models import ProyectoEvaluacion, ActivoDigital, Riesgo, TratamientoRiesgo

class ProyectoEvaluacionForm(forms.ModelForm):
    class Meta:
        model = ProyectoEvaluacion
        fields = '__all__'

class ActivoDigitalForm(forms.ModelForm):
    class Meta:
        model = ActivoDigital
        fields = [
            'nombre',
            'tipo',
            'descripcion',
            'c',
            'i',
            'd',
            'nivel_criticidad',
            'fuente_osint',
            'estado',
        ]


class ShodanBusquedaForm(forms.Form):
    objetivo = forms.CharField(
        label='IP o dominio',
        max_length=255,
        help_text='Ingrese una IP pública o un dominio'
    )


class RiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = [
            'activo',
            'amenaza',
            'vulnerabilidad',
            'probabilidad',
            'impacto',
        ]
        exclude = (
            'nivel_riesgo',
            'nivel_prioridad',
            'nivel_riesgo_residual'
        )
        
class TratamientoRiesgoForm(forms.ModelForm):
    probabilidad_residual = forms.IntegerField(min_value=1, max_value=5)
    impacto_residual = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = TratamientoRiesgo
        exclude = ('riesgo',)

class RiesgoEdicionForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = [
            'probabilidad_residual',
            'impacto_residual',
            'estado'
        ]

    def clean(self):
        cleaned_data = super().clean()
        p = cleaned_data.get('probabilidad_residual')
        i = cleaned_data.get('impacto_residual')

        if (p and not i) or (i and not p):
            raise forms.ValidationError(
                'Debe ingresar probabilidad e impacto residual juntos.'
            )

        return cleaned_data
