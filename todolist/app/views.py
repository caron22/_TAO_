from django.shortcuts import render, redirect
from .models import Task , Centro_costos, Concepto
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.urls import reverse
from .forms import ConceptoForm
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .forms import RegistroForm,DetalleForm
from .models import Grupos_detalle, Grupos_registro
from django.db import models  # Agrega esta línea
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from django.forms.utils import ErrorList
# from django.template import loader
# Create your views here.

def index(request):
   
    return render(request, "app/index.html")

def unidad_medida_view(request):
    # template = loader.get_template("app/index.html")
    db_data = Task.objects.all()
    context = {
        "db_data": db_data[::-1],
        "update": None
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "app/unidad_medida.html", context)

def insert(request):
    try:
        task_subject = request.POST["subject"]
        
        if task_subject == "":
            raise ValueError("El texto no puede estar en vacio.")
        db_data = Task(subject=task_subject)
        db_data.save()
        return HttpResponseRedirect(reverse("unidad_medida")) 
    except ValueError as err:
        print(err)
        return HttpResponseRedirect(reverse("unidad_medida")) 

def update(request):
    task_id = request.POST["id"]
    task_subject = request.POST["subject"]
   
    db_data = Task.objects.get(pk=task_id)
    db_data.subject = task_subject
    db_data.save()
    return HttpResponseRedirect(reverse("unidad_medida")) 

def update_form(request, task_id):
    db_data = Task.objects.all()
    db_data_only = Task.objects.get(pk=task_id)
    print(db_data_only)
    context = {
        "db_data": db_data[::-1],
        "update": db_data_only
    }
    return render(request, "app/unidad_medida.html", context)

def delete(request, task_id):
    db_data = Task.objects.filter(id=task_id)
    db_data.delete()
    return HttpResponseRedirect(reverse("unidad_medida")) 
#------------------------------------------------------------------

def centrodecostos_view(request):
    db_data = Centro_costos.objects.all()
    subjects = Task.objects.all()  # Obtén todos los datos de la tabla Subject
    #numero_id = {trae_id.id: trae_id.subject for trae_id in Task.objects.all()}
    
    #for id, subject in numero_id.items():
        #print(f"ID: {id}, Subject: {subject}")
              
    context = {
        "db_data": db_data[::-1],
        "update": None,
        "subjects": subjects,  # Agrega los subjects al contexto
        #"numero_id": numero_id, 
    }
    return render(request, "app/Centrodecostos.html", context)



def centrodecostos_delete(request, centro_costos_id):
    db_data = Centro_costos.objects.filter(id=centro_costos_id)
    db_data.delete()
    return HttpResponseRedirect(reverse("centrodecostos_view"))

'''def centrodecostos_insert(request):
    try:
        Centro_costos_unidad = request.POST["unidad"]
        Centro_costos_descripcion = request.POST["descripcion"]
        if Centro_costos_unidad == "" or Centro_costos_descripcion == "":
            raise ValueError("El texto no puede estar en vacio.")
        db_data = Centro_costos(unidad=Centro_costos_unidad, descripcion=Centro_costos_descripcion)
        db_data.save()
        return HttpResponseRedirect(reverse("centrodecostos_view")) 
    except ValueError as err:
        print(err)
        return HttpResponseRedirect(reverse("centrodecostos_view")) '''



def centrodecostos_insert(request):
    try:
        Centro_costos_unidad = request.POST["unidad"]
        Centro_costos_task_id = request.POST["task_id"]
        
        if Centro_costos_unidad == "" or Centro_costos_task_id == "":
            raise ValueError("El texto no puede estar en vacío.")
        
        # Obtén la tarea correspondiente
        tarea = Task.objects.get(id=Centro_costos_task_id)
        
        # Crea el nuevo registro de Centro_costos con la tarea asociada
        db_data = Centro_costos(unidad=Centro_costos_unidad, task=tarea)
        db_data.save()
        
        return HttpResponseRedirect(reverse("centrodecostos_view")) 
    except (Task.DoesNotExist, ValueError) as err:
        print(err)
        return HttpResponseRedirect(reverse("centrodecostos_view"))


def centrodecostos_update(request):
    centro_costos_id = request.POST["id"]
    Centro_costos_unidad = request.POST["unidad"]
    Centro_costos_task_id = request.POST["task_id"]
    db_data = Centro_costos.objects.get(pk=centro_costos_id)
    db_data.unidad = Centro_costos_unidad
    db_data.task_id = Centro_costos_task_id  # Corregido aquí
    db_data.save()
    return HttpResponseRedirect(reverse("centrodecostos_view"))


def centrodecostos_update_form(request, centro_costos_id):
    db_data = Centro_costos.objects.all()
    db_data_only = Centro_costos.objects.get(pk=centro_costos_id)
    subjects = Task.objects.all()

    # Imprime los datos de las tareas en la consola del servidor Django
    for tarea in subjects:
        print(f'Task ID: {tarea.id}, Task Subject: {tarea.subject}')

    context = {
        "db_data": db_data[::-1],
        "centrodecostos_update_form": db_data_only,
        "subjects": subjects,
    }

    return render(request, "app/Centrodecostos.html", context)

#--------------------------




#----------CONCEPTOS PRUEBAS----------------



def conceptos_insert_sinusocreo(request):
    try:
        codigo_ex = request.POST.get("codigo_ex")
        
        task_id = request.POST.get("task_id")
        centro_costos_id = request.POST.get("centro_costos_id")
        grupos_detalle_id = request.POST.get("grupos_detalle_id")
        print("paso por aca")
        if codigo_ex == "" or task_id is None or (centro_costos_id and grupos_detalle_id):
            raise ValueError("Los campos no pueden estar vacíos y solo se puede seleccionar uno de los dos campos: centro_costos o grupos_detalle.")
        if grupos_detalle_id:
                grupos_detalle = Grupos_detalle.objects.get(id=grupos_detalle_id)
                porcentaje_acumulado = grupos_detalle.porcentaje_acumulado
                if porcentaje_acumulado < 100:
                    raise ValueError("El grupo seleccionado no tiene el 100% en Grupos_detalle.")


        tarea = Task.objects.get(id=task_id)
        centro_costos = Centro_costos.objects.get(id=centro_costos_id)
        grupos_detalle = Grupos_detalle.objects.get(id=grupos_detalle_id)

        nuevo_concepto = Concepto(
            codigo_ex=codigo_ex,
            task=tarea,
            centro_costos=centro_costos,
            grupos_detalle=grupos_detalle,
        )
        nuevo_concepto.save()

        return HttpResponseRedirect(reverse("conceptos_view"))
    except (Task.DoesNotExist, Centro_costos.DoesNotExist, Grupos_detalle.DoesNotExist, ValueError) as err:
        print(err)
        return HttpResponseRedirect(reverse("conceptos_view"))



def conceptos_delete(request, conceptosForm_id):
    db_data = Concepto.objects.filter(id=conceptosForm_id)
    db_data.delete()
    return HttpResponseRedirect(reverse("conceptos_view"))

from django.shortcuts import render, redirect
from .forms import ConceptoForm
from django.contrib import messages
from .models import Concepto, Grupos_detalle, Centro_costos

def conceptos_view(request):
    print("paso por aca")
    if request.method == 'POST':
        print("paso por aca11")
        form = ConceptoForm(request.POST)
   
        if form.is_valid():
            grupos_detalle = form.cleaned_data.get('grupos_detalle')
            centro_costos = form.cleaned_data.get('centro_costos')

            if not centro_costos and not grupos_detalle:
                messages.success(request, 'Debe seleccionar al menos un campo.', extra_tags='custom-error-campo')
            elif centro_costos and grupos_detalle:
                print("Solo se puede seleccionar uno de los dos campos.")
                messages.success(request, 'Solo se puede seleccionar uno de los dos campos.', extra_tags='custom-error-campo-uno')
            elif grupos_detalle:
                porcentaje_acumulado = grupos_detalle.porcentaje_acumulado
                if porcentaje_acumulado < 100:
                    print("El grupo seleccionado no tiene el 100% ")
                    messages.success(request, 'El grupo seleccionado no tiene el 100% ', extra_tags='custom-error-campo-100')
                
            if not messages.get_messages(request):
                form.save()
                print( "Concepto guardado exitosamente.")
                messages.success(request, 'Concepto guardado exitosamente.', extra_tags='custom-ok')
                return redirect('conceptos_view')
    else:
        form = ConceptoForm()

    grupos_detalle_filtros = Grupos_detalle.objects.all()
    centro_costos_filtros = Centro_costos.objects.all()

    context = {
        'form': form,
        'db_data': Concepto.objects.all(),
        'Grupos_detalle_filtros': grupos_detalle_filtros,
        'Centro_costos_filtros': centro_costos_filtros,
    }

    return render(request, 'app/conceptos.html', context)


def conceptos_edit(request, conceptosForm_id):
    concepto = get_object_or_404(Concepto, id=conceptosForm_id)
    form = ConceptoForm(request.POST, instance=concepto)

    if form.is_valid(): 
        if form.is_valid():
            grupos_detalle = form.cleaned_data.get('grupos_detalle')
            centro_costos = form.cleaned_data.get('centro_costos')

            if not centro_costos and not grupos_detalle:
                messages.success(request, 'Debe seleccionar al menos un campo.', extra_tags='custom-error-campo')
            elif centro_costos and grupos_detalle:
                print("Solo se puede seleccionar uno de los dos campos.")
                messages.success(request, 'Solo se puede seleccionar uno de los dos campos.', extra_tags='custom-error-campo-uno')
            elif grupos_detalle:
                porcentaje_acumulado = grupos_detalle.porcentaje_acumulado
                if porcentaje_acumulado < 100:
                    print("El grupo seleccionado no tiene el 100% ")
                    messages.success(request, 'El grupo seleccionado no tiene el 100% ', extra_tags='custom-error-campo-100')
                
            if not messages.get_messages(request):
                form.save()
                print( "Concepto guardado exitosamente.")
                messages.success(request, 'Concepto guardado exitosamente.', extra_tags='custom-ok')
                form.save()
                return redirect('conceptos_view')
            
        
        #return redirect('conceptos_view')  # Cambiar a la vista principal si la edición es exitosa
    else:
        form = ConceptoForm(instance=concepto)

    grupos_detalle_filtros = Grupos_detalle.objects.all()  # Obtener todos los grupos_detalle

    context = {
        'form': form,
        'db_data': Concepto.objects.all(),
        'Unidad_medida_filtros': Task.objects.all(),
        'Grupos_detalle_filtros': grupos_detalle_filtros,  # Pasar grupos_detalle a la plantilla
        'edit_mode': True,
        'edit_id': conceptosForm_id,
    }

    return render(request, 'app/conceptos.html', context)


#--------------------------

def editar_registro(request, pk):
    detalle = get_object_or_404(Grupos_detalle, pk=pk)
    registros = Grupos_registro.objects.filter(detalle=detalle)
    total_porcentaje = registros.aggregate(models.Sum('porcentaje'))['porcentaje__sum'] or 0
    grupos_detalles = Grupos_detalle.objects.all()

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nuevo_porcentaje = form.cleaned_data['porcentaje']
            nuevo_centro_costos = form.cleaned_data['centro_costos']

            # Restar el porcentaje anterior
            porcentaje_anterior = registros.aggregate(models.Sum('porcentaje'))['porcentaje__sum'] or 0
            detalle.porcentaje_acumulado -= porcentaje_anterior

            # Sumar el nuevo porcentaje
            detalle.porcentaje_acumulado += nuevo_porcentaje

            if detalle.porcentaje_acumulado > 100:
                raise ValidationError("El porcentaje total excede el 100%. Por favor, revisa y ajusta los valores.")

            detalle.save()

            for registro in registros:
                registro.porcentaje = nuevo_porcentaje
                registro.centro_costos = nuevo_centro_costos
                registro.save()

            return redirect('agregar_registro')

    else:
        form = RegistroForm()

    return render(request, 'app/agregar_registro.html', {
        'form': form,
        'detalle': detalle,
        'registros': registros,
        'total_porcentaje': total_porcentaje,
        'falta_porcentaje': 100 - total_porcentaje,
        'grupos_detalles': grupos_detalles
    })





#----------GRUPOS SENTROS----------------
def agregar_detalle(request):
    if request.method == 'POST':
        form = DetalleForm(request.POST)
        if form.is_valid():
            Grupos_detalle.objects.create(nombre=form.cleaned_data['nombre'])
            return redirect('agregar_detalle')
    else:
        form = DetalleForm()

    return render(request, 'app/grupos_centros.html', {'form': form})


def agregar_registro(request):

    #detalles = Grupos_detalle.objects.all()
    registros = Grupos_registro.objects.all()
    total_porcentaje = registros.aggregate(models.Sum('porcentaje'))['porcentaje__sum'] or 0
    grupos_detalles = Grupos_detalle.objects.all()

    if request.method == 'POST':
        detalle_form = DetalleForm(request.POST)
        form = RegistroForm(request.POST)

        try:
            if detalle_form.is_valid():
                detalle_nombre = detalle_form.cleaned_data['nombre']

                if detalle_nombre:
                    nuevo_grupo = Grupos_detalle.objects.create(nombre=detalle_nombre)
                    messages.success(request, 'Grupo agregado con éxito.')
                    detalle_form = DetalleForm() #Limpia el registro de detalle_form
                    return redirect('grupos_centros')

            if form.is_valid():
                detalle = form.cleaned_data['detalle']
                porcentaje = form.cleaned_data['porcentaje']
                centro_costos = form.cleaned_data['centro_costos']
                print(f"Centro de costos: {centro_costos}")

              
                if porcentaje <= 0:
                    #form.errors['centro_costos'] = form.error_class(["El porcentaje no puede ser negativo."])
                    messages.success(request, 'El porcentaje no pueden ser menor o igual a 0', extra_tags='custom-error')
                    detalle_form = DetalleForm() #Limpia el registro de detalle_form
                    raise ValidationError("Algo salio mal")
      
                if centro_costos is None:
                    #form.errors['centro_costos'] = form.error_class(["Por favor, selecciona un centro de costos."])
                    messages.success(request, 'Por favor, selecciona un centro de costos.', extra_tags='custom-error')
                    detalle_form = DetalleForm() #Limpia el registro de detalle_form
                    raise ValidationError("Algo salio mal")
                
                
                detalle_obj = get_object_or_404(Grupos_detalle, pk=detalle.pk)
                porcentaje_acumulado = detalle_obj.porcentaje_acumulado + porcentaje

                if porcentaje_acumulado > 100:
                    #form.errors['porcentaje'] = form.error_class(["Por favor, El porcentaje total excede el 100%. Por favor, revisa y ajusta los valores."])
                    messages.success(request, 'Por favor, El porcentaje total excede el 100%. Por favor, revisa y ajusta los valores.', extra_tags='custom-error')
                    detalle_form = DetalleForm() #Limpia el registro de detalle_form
                    raise ValidationError("Algo salio mal")
                
                detalle_obj.porcentaje_acumulado = porcentaje_acumulado
                detalle_obj.save()

                Grupos_registro.objects.create(
                    detalle=detalle_obj,
                    porcentaje=porcentaje,
                    centro_costos=centro_costos,
                )
                #form = RegistroForm()  # Reinicializar el formulario
                #form.errors['ok'] = form.error_class(["Se agregó un registro exitosamente."])
                #detalle_form = DetalleForm() #Limpia el registro de detalle_form
                messages.success(request, 'Se agregó un registro exitosamente', extra_tags='custom-success')
                return redirect('grupos_centros')#Redirecciona para evitar mas guardados con f5
            
        except ValidationError as e:
            messages.error(request, str(e))

    else:
        form = RegistroForm()
        detalle_form = DetalleForm()

    return render(request, 'app/grupos_centros.html', {
        'form': form,
        'detalle_form': detalle_form,
        #'detalles': detalles,
        'registros': registros,
        'total_porcentaje': total_porcentaje,
        'falta_porcentaje': 100 - total_porcentaje,
        'grupos_detalles': grupos_detalles
    })



def eliminar_registro(request, pk):
    registro = get_object_or_404(Grupos_registro, pk=pk)
    detalle = registro.detalle
    detalle.porcentaje_acumulado -= registro.porcentaje
    detalle.save()
    registro.delete()
    return redirect('grupos_centros')


def grupos_edit(request, pk):
    detalle = get_object_or_404(Grupos_detalle, pk=pk)

    if request.method == 'POST':
        # Si es una solicitud POST, significa que se envió el formulario de edición
        form = RegistroForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            # Puedes agregar un mensaje de éxito si lo deseas
            return redirect('grupos_centros')
    else:
        # Si es una solicitud GET, muestra el formulario prellenado con los datos actuales
        form = RegistroForm(instance=detalle)

    return render(request, 'app/grupos_centros.html', {'form': form, 'detalle': detalle})


def grupos_update(request, gruposForm_id):
    instance = get_object_or_404(Grupos_detalle, id=gruposForm_id)
    form = RegistroForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('grupos_centros')  # Cambia 'tu_nombre_url_lista' con el nombre de tu URL para la lista
    return render(request, 'app/grupos_centros.html', {'form': form, 'instance': instance})

def grupos_delete(request, gruposForm_id):
    db_data = Grupos_detalle.objects.filter(id=gruposForm_id)
    db_data.delete()
    return HttpResponseRedirect(reverse("grupos_centros"))

def grupos_deletegrupos_delete(request, gruposForm_id):
    try:
        grupo_detalle = Grupos_detalle.objects.get(id=gruposForm_id)
        grupo_detalle.porcentaje_acumulado = 0
        grupo_detalle.save()

        # Además, si deseas eliminar los registros asociados en Grupos_registro, puedes hacerlo de la siguiente manera:
        Grupos_registro.objects.filter(detalle=grupo_detalle).delete()

        return HttpResponseRedirect(reverse("grupos_centros"))
    except Grupos_detalle.DoesNotExist:
        # Manejar el caso en el que no se encuentre la instancia de Grupos_detalle con el ID proporcionado
        return HttpResponseNotFound("No se encontró el grupo con el ID proporcionado.")



