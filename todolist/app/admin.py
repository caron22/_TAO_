from django.contrib import admin

# Register your models here.


# Register your models here.
from . import models
admin.site.register(models.Task)

admin.site.register(models.Centro_costos)
admin.site.register(models.Concepto)
admin.site.register(models.Grupos_detalle)
admin.site.register(models.Grupos_registro)
