from django import forms
from .models import Concepto,Grupos_registro,Grupos_detalle
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib import messages
class DetalleForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        required=True,
        label='<b>Descripcion grupo</b>',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
 

class RegistroForm(forms.ModelForm):
    # ... Resto del código del formulario ...

    class Meta:
        model = Grupos_registro
        fields = ['detalle', 'centro_costos', 'porcentaje']
        
        widgets = {
            'detalle': forms.Select(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'step': 1 ,'class': 'form-control'}),
            'centro_costos': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['centro_costos'].label_from_instance = lambda obj: f"{obj.unidad}"

    def as_custom_p(self):
        # Selecciona los campos que deseas incluir en el formato personalizado
        fields = ['detalle', 'centro_costos', 'porcentaje']
        return self._html_output(
            normal_row=self._html_output(fields, 'form-row', 'form-row', 'form-group'),
            error_row='%s',
            row_ender='</div>',
            help_text_html=' %s',
            errors_on_separate_row=True,
        )

  
    
       


    ''' def clean_porcentaje(self):
        porcentaje = self.cleaned_data['porcentaje']
        detalle = self.cleaned_data['detalle']
        centro_costos = self.cleaned_data.get('centro_costos')
        porcentaje_acumulado = detalle.porcentaje_acumulado + porcentaje
        if  centro_costos is None:
            raise forms.ValidationError("Por favor, selecciona un centro de costos.")
        if porcentaje_acumulado > 100:
            raise forms.ValidationError("El porcentaje total excede el 100%.")
        
        return porcentaje
       '''

#--------------------------------------------------
from django import forms

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['codigo_ex', 'centro_costos', 'grupos_detalle']
        labels = {
            'codigo_ex': 'CodigoExterno:',
            'centro_costos': 'Centro de costos :',
            'grupos_detalle': 'Grupo :',
        }

        widgets = {
            'codigo_ex': forms.TextInput(attrs={'class': 'form-control'}),
            'centro_costos': forms.Select(attrs={'class': 'form-control'}),
            'grupos_detalle': forms.Select(attrs={'class': 'form-control'}),
        }
    
   
#--------------------------
