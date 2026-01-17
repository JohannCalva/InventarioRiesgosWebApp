from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProyectoEvaluacion(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_organizacion = models.CharField(max_length=100)
    responsable = models.CharField(max_length=150)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre


class ActivoDigital(models.Model):

    TIPO_ACTIVO_CHOICES = [
        ('Dominio', 'Dominio'),
        ('Subdominio', 'Subdominio'),
        ('IP Pública', 'IP Pública'),
        ('Servicio Expuesto', 'Servicio Expuesto'),
        ('Aplicación Web', 'Aplicación Web'),
        ('API', 'API'),
        ('Repositorio Público', 'Repositorio Público'),
        ('Certificado Digital', 'Certificado Digital'),
        ('Archivo Indexado', 'Archivo Indexado'),
        ('Credencial Filtrada', 'Credencial Filtrada'),
    ]

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Desconocido', 'Desconocido'),
    ]

    proyecto = models.ForeignKey(
        ProyectoEvaluacion,
        on_delete=models.CASCADE,
        related_name='activos'
    )
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPO_ACTIVO_CHOICES)
    descripcion = models.TextField(blank=True)

    c = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    i = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    d = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    cia_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        editable=False
    )

    nivel_criticidad = models.CharField(max_length=20, blank=True)
    fuente_osint = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_identificacion = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.cia_promedio = round((self.c + self.i + self.d) / 3, 2)
        
        if self.cia_promedio >= 4:
            self.nivel_criticidad = 'Alta'
        elif self.cia_promedio >= 2:
            self.nivel_criticidad = 'Media'
        else:
            self.nivel_criticidad = 'Baja'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Amenaza(models.Model):

    TIPO_CHOICES = [
        ('Interna', 'Interna'),
        ('Externa', 'Externa'),
    ]

    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Vulnerabilidad(models.Model):

    TIPO_CHOICES = [
        ('Técnica', 'Técnica'),
        ('Configuración', 'Configuración'),
        ('Proceso', 'Proceso'),
        ('Humana', 'Humana'),
    ]

    descripcion = models.TextField()
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    criterio_deteccion = models.TextField()

    def __str__(self):
        return f"{self.tipo} - {self.descripcion[:50]}"


class Riesgo(models.Model):

    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En tratamiento', 'En tratamiento'),
        ('Cerrado', 'Cerrado'),
    ]

    activo = models.ForeignKey(
        ActivoDigital,
        on_delete=models.CASCADE,
        related_name='riesgos'
    )
    amenaza = models.ForeignKey(Amenaza, on_delete=models.PROTECT)
    vulnerabilidad = models.ForeignKey(Vulnerabilidad, on_delete=models.PROTECT)

    # Valoración inicial
    probabilidad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    impacto = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    nivel_riesgo = models.IntegerField(editable=False)

    # Riesgo residual
    probabilidad_residual = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    impacto_residual = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    nivel_riesgo_residual = models.IntegerField(
        null=True, blank=True
    )

    nivel_prioridad = models.CharField(
        max_length=10,
        editable=False
    )

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')

    def save(self, *args, **kwargs):
        # Riesgo inherente
        self.nivel_riesgo = self.probabilidad * self.impacto

        if self.nivel_riesgo <= 6:
            self.nivel_prioridad = 'Baja'
        elif self.nivel_riesgo <= 14:
            self.nivel_prioridad = 'Media'
        else:
            self.nivel_prioridad = 'Alta'

        # Riesgo residual
        if self.probabilidad_residual and self.impacto_residual:
            self.nivel_riesgo_residual = (
                self.probabilidad_residual * self.impacto_residual
            )

        super().save(*args, **kwargs)



    def __str__(self):
        return f"Riesgo - {self.activo.nombre}"

    def get_color_class(self):
        """Devuelve la clase de color de Bootstrap según el nivel de riesgos."""
        if self.nivel_prioridad == 'Alta':
            return 'danger'
        elif self.nivel_prioridad == 'Media':
            return 'warning'
        else:
            return 'success'


class TratamientoRiesgo(models.Model):

    ESTRATEGIA_CHOICES = [
        ('Mitigar', 'Mitigar'),
        ('Transferir', 'Transferir'),
        ('Aceptar', 'Aceptar'),
        ('Evitar', 'Evitar'),
    ]

    riesgo = models.OneToOneField(
        Riesgo,
        on_delete=models.CASCADE,
        related_name='tratamiento'
    )
    estrategia = models.CharField(max_length=20, choices=ESTRATEGIA_CHOICES)
    descripcion_control = models.TextField()
    control_iso_27002 = models.CharField(max_length=100)
    responsable = models.CharField(max_length=150)
    fecha_implementacion = models.DateField()

    def __str__(self):
        return f"Tratamiento - {self.riesgo}"
