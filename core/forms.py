from django import forms
from .models import ProyectoEvaluacion, ActivoDigital, Riesgo, TratamientoRiesgo


class ProyectoEvaluacionForm(forms.ModelForm):
    class Meta:
        model = ProyectoEvaluacion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_organizacion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
        }

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
            'fuente_osint',
            'estado',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'c': forms.NumberInput(attrs={'class': 'form-control'}),
            'i': forms.NumberInput(attrs={'class': 'form-control'}),
            'd': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuente_osint': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class ActivoDigitalEdicionForm(forms.ModelForm):
    class Meta:
        model = ActivoDigital
        fields = [
            'nombre',
            'tipo',
            'descripcion',
            'c',
            'i',
            'd',
            'estado',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'c': forms.NumberInput(attrs={'class': 'form-control'}),
            'i': forms.NumberInput(attrs={'class': 'form-control'}),
            'd': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class ShodanBusquedaForm(forms.Form):
    objetivo = forms.CharField(
        label='IP o dominio',
        max_length=255,
        help_text='Ingrese una IP pública o un dominio',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej. 8.8.8.8 o dns.google'})
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
        widgets = {
            'activo': forms.Select(attrs={'class': 'form-select'}),
            'amenaza': forms.Select(attrs={'class': 'form-select'}),
            'vulnerabilidad': forms.Select(attrs={'class': 'form-select'}),
            'probabilidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'impacto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
        
class TratamientoRiesgoForm(forms.ModelForm):
    probabilidad_residual = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    impacto_residual = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TratamientoRiesgo
        exclude = ('riesgo',)
        widgets = {
            'estrategia': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_control': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'control_iso_27002': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_implementacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RiesgoEdicionForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = [
            'probabilidad_residual',
            'impacto_residual',
            'estado'
        ]
        widgets = {
            'probabilidad_residual': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'impacto_residual': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p = cleaned_data.get('probabilidad_residual')
        i = cleaned_data.get('impacto_residual')

        if (p and not i) or (i and not p):
            raise forms.ValidationError(
                'Debe ingresar probabilidad e impacto residual juntos.'
            )

        return cleaned_data
