
(function(){


    

    document.addEventListener('DOMContentLoaded', function () {
        var eliminarBotones = document.querySelectorAll('.eliminarConfirmacion');
    
        eliminarBotones.forEach(function (boton) {
            boton.addEventListener('click', function (event) {
                var confirmacion = confirm('¿Estás seguro de que quieres eliminar esta fila?');
    
                if (!confirmacion) {
                    event.preventDefault(); // Cancela la acción predeterminada si el usuario elige no confirmar
                }
            });
        });
    });

    formulario.addEventListener('submit',function (e) {
        let centrocostos = String(unidad.value).trim();
        
        if(centrocostos.length === 0 ){
            Swal.fire({
                position: "center",
                icon: "warning",
                title: "El campo esta vacio",
                showConfirmButton: false,
                timer: 1500
              });
            e.preventDefault();
        }
    });

    formulario.addEventListener('submit',function (e) {
        let unidadmedida = String(subject.value).trim();
        
        if(unidadmedida.length === 0 ){
            Swal.fire({
                position: "center",
                icon: "warning",
                title: "El campo esta vacio",
                showConfirmButton: false,
                timer: 1500
              });
            e.preventDefault();
        }
        
    });

   
}
)();


