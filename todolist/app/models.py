from django.db import models

from django.db import models

class Task(models.Model):
    subject = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.subject

class Centro_costos(models.Model):
    unidad = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='centro_costos')

    def __str__(self):
        return self.unidad

class Grupos_detalle(models.Model):
    nombre = models.CharField(max_length=255)
    porcentaje_acumulado = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class Grupos_registro(models.Model):
    detalle = models.ForeignKey(Grupos_detalle, on_delete=models.CASCADE)
    centro_costos = models.ForeignKey(Centro_costos, on_delete=models.SET_NULL, null=True, blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.detalle)

class Concepto(models.Model):
    codigo_ex = models.CharField(max_length=100)

    centro_costos = models.ForeignKey(Centro_costos, on_delete=models.CASCADE, related_name='conceptos', null=True, blank=True)
    grupos_detalle = models.ForeignKey(Grupos_detalle, on_delete=models.CASCADE, related_name='grupos_detalle', null=True, blank=True)

    def __str__(self):
        return self.codigo_ex
    

