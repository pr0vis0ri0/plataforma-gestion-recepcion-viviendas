from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from proyectos.models import Proyecto, Vivienda, Recinto
import os

def validate_file_size(file):
    """Valida que el archivo no supere los 10MB"""
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'El archivo no puede superar los {max_size_mb}MB')

def validate_file_extension(file):
    """Valida que el archivo sea PDF, DOC, DOCX o imagen"""
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if ext not in valid_extensions:
        raise ValidationError(f'Tipo de archivo no permitido. Solo se permiten: {", ".join(valid_extensions)}')

class TipoObservacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Observación"
        verbose_name_plural = "Tipos de Observación"

class EstadoObservacion(models.Model):
    codigo = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50, unique=True)  # También único por nombre
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Estado de Observación"
        verbose_name_plural = "Estados de Observación"
        constraints = [
            models.UniqueConstraint(
                fields=["codigo", "nombre"], 
                name="uniq_estado_codigo_nombre"
            )
        ]
        indexes = [
            models.Index(fields=["activo"]),
            models.Index(fields=["codigo", "activo"]),
        ]

class Observacion(models.Model):
    # Usar TextChoices para mejor validación
    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        URGENTE = "URGENTE", "Urgente"

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='observaciones')
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, related_name='observaciones')
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE, blank=True, null=True)

    elemento = models.CharField(max_length=200, help_text="Elemento observado (ej: Pintura, Grifería)")
    detalle = models.TextField(help_text="Descripción detallada de la observación")
    tipo = models.ForeignKey(TipoObservacion, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoObservacion, on_delete=models.PROTECT)

    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA)
    es_urgente = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    # Proteger usuarios importantes, permitir SET_NULL para flexibilidad
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, 
                                   related_name='observaciones_creadas')
    asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='observaciones_asignadas')

    # Seguimiento
    observaciones_seguimiento = models.TextField(blank=True, help_text="Notas de seguimiento")
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    # Archivo adjunto
    archivo_adjunto = models.FileField(
        upload_to='observaciones/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_file_size, validate_file_extension],
        help_text="Archivo adjunto (PDF, DOC, DOCX, JPG, PNG, GIF - máx. 10MB)"
    )

    def __str__(self):
        return f"{self.proyecto.codigo} - {self.vivienda.codigo} - {self.elemento}"

    @property
    def esta_vencida(self):
        if self.fecha_vencimiento and self.estado.nombre == 'Abierta':
            from datetime import date
            return date.today() > self.fecha_vencimiento
        return False

    @property
    def dias_para_vencer(self):
        if self.fecha_vencimiento and self.estado.nombre == 'Abierta':
            from datetime import date
            delta = self.fecha_vencimiento - date.today()
            return delta.days
        return None
    id_externo = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="ID externo para importación"
    )
    
    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ['-fecha_creacion']
        # Índices optimizados para consultas frecuentes
        indexes = [
            models.Index(fields=['id_externo']),
            models.Index(fields=["estado", "fecha_vencimiento"]),  # Consultas de vencimiento
            models.Index(fields=["proyecto", "vivienda"]),         # Filtros por proyecto/vivienda
            models.Index(fields=["asignado_a", "estado"]),         # Consultas por asignado
            models.Index(fields=["fecha_ultima_actualizacion"]),   # Ordenamiento temporal
            models.Index(fields=["prioridad", "es_urgente"]),      # Filtros de prioridad
            models.Index(fields=["creado_por", "fecha_creacion"]), # Historiales por usuario
        ]
        # Validaciones de integridad
        constraints = [
            # Validar fechas lógicas
            models.CheckConstraint(
                check=models.Q(fecha_cierre__isnull=True) | 
                      models.Q(fecha_cierre__gte=models.F('fecha_creacion')),
                name="chk_fecha_cierre_despues_creacion"
            ),
            models.CheckConstraint(
                check=models.Q(fecha_vencimiento__isnull=True) |
                      models.Q(fecha_vencimiento__gte=models.F('fecha_creacion__date')),
                name="chk_fecha_vencimiento_despues_creacion"
            ),
        ]

class ArchivoAdjuntoObservacion(models.Model):
    observacion = models.ForeignKey(Observacion, on_delete=models.CASCADE, related_name='archivos_adjuntos')
    archivo = models.FileField(
        upload_to='observaciones/%Y/%m/',
        validators=[validate_file_size, validate_file_extension],
        help_text="Archivo adjunto (PDF, DOC, DOCX, JPG, PNG, GIF - máx. 10MB)"
    )
    nombre_original = models.CharField(max_length=255, blank=True)
    descripcion = models.CharField(max_length=255, blank=True, help_text="Descripción opcional del archivo")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        if not self.nombre_original and self.archivo:
            self.nombre_original = self.archivo.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.observacion.pk} - {self.nombre_original}"
    
    class Meta:
        verbose_name = "Archivo Adjunto"
        verbose_name_plural = "Archivos Adjuntos"
        ordering = ['-fecha_subida']

class SeguimientoObservacion(models.Model):
    observacion = models.ForeignKey(Observacion, on_delete=models.CASCADE, related_name='seguimientos')
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    accion = models.CharField(max_length=100)
    comentario = models.TextField(blank=True)
    estado_anterior = models.ForeignKey(EstadoObservacion, on_delete=models.PROTECT, 
                                       related_name='seguimientos_desde', null=True, blank=True)
    estado_nuevo = models.ForeignKey(EstadoObservacion, on_delete=models.PROTECT, 
                                    related_name='seguimientos_hacia', null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.observacion} - {self.accion} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Seguimiento de Observación"
        verbose_name_plural = "Seguimientos de Observaciones"
        ordering = ['-fecha']
        # Índices para optimizar consultas frecuentes
        indexes = [
            models.Index(fields=["observacion", "fecha"]),
            models.Index(fields=["usuario", "fecha"]),
        ]
        # Sin restricciones de estado por ahora para permitir flexibilidad
