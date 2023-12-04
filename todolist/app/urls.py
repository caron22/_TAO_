from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("unidad_medida/", views.unidad_medida_view, name="unidad_medida"),
    path("insert/", views.insert, name="insert"),
    path("update", views.update, name="update"),
    path("update/<int:task_id>", views.update_form, name="update_form"),
    path("delete/<int:task_id>", views.delete, name="delete"),
    
    path("centrodecostos/", views.centrodecostos_view, name='centrodecostos_view'),
    path("centrodecostos_insert/", views.centrodecostos_insert, name="centrodecostos_insert"),
    path("centrodecostos_update", views.centrodecostos_update, name="centrodecostos_update"),
    path("centrodecostos_update_form/<int:centro_costos_id>", views.centrodecostos_update_form, name="centrodecostos_update_form"),
    path("centrodecostos_delete/<int:centro_costos_id>", views.centrodecostos_delete, name="centrodecostos_delete"),
   
    #path("conceptos/", views.conceptos_view, name='conceptos_view'),

    #path("conceptos_insert/", views.conceptos_insert, name="conceptos_insert"),
    path("concepto/", views.conceptos_view, name='conceptos_view'),
    path("conceptos_delete/<int:conceptosForm_id>", views.conceptos_delete, name="conceptos_delete"),
    path("conceptos_edit/<int:conceptosForm_id>", views.conceptos_edit, name="conceptos_edit"),




    
    path('eliminar_registro/<int:pk>/', views.eliminar_registro, name='eliminar_registro'),
    path('grupos_centros/', views.agregar_registro, name='grupos_centros'),
    path('grupos_edit/<int:pk>/', views.grupos_edit, name='grupos_edit'),
    path('grupos_delete/<int:gruposForm_id>', views.grupos_delete, name='grupos_delete'),



]