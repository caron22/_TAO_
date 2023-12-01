# To Do List - Django
Este es un pequeño proyecto realizado con el framework de Django para desarrollo web, puedes ver el video de este proyecto [aquí][gvc]. Aquí se presenta una simple aplicación de To Do List para ejemplificar un CRUD completo y mostrar varias de las funcionalidades que Django tiene para ofrecer.

## Tecnologías:
- Python
- Django
- HTML
- Jinja2

## ¿Como correr el proyecto?
**1:** Clonar el repositorio con el comando de git:
```
git clone <dirección del repo>
```
**2:** Ingresar desde la terminal dentro de la carpeta del proyecto. Ejemplo en linux:
```
cd <nombre del directorio>
```
**3:** Crear un entorno virtual:
```
python -m venv venv
```
**4:** Ingresar en el entorno virtual:
- Para linux y Mac:
```
source venv/bin/activate
```
- Para Window:
```
venv\Scripts\activate.bat
```
**5:** Descargar las dependencias del archivo 'requirements.txt' con el comando:
```
pip install -r requirements.txt   
```
**6:** Ingresar en la carpeta del proyecto Django:
```
cd <nombre del proyecto Django>
```
**7:** Ejecutar el servidor de desarrollo de Django:
```
python manage.py runserver
```
**8:** En el navegador ir al localhost:8000.


[gvc]:https://youtu.be/FSy_iTibXfU




Datatable:

let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    //scrollX: "2000px",
    lengthMenu: [5, 10, 15, 20, 100, 200, 500],
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [1] }
        //{ width: "50%", targets: [0] }
    ],
    pageLength: 3,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listUsers();

    dataTable = $("#datatable_users").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listUsers = async () => {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();

        let content = ``;
        users.forEach((user, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>${user.address.city}</td>
                    <td>${user.company.name}</td>
                    <td><i class="fa-solid fa-check" style="color: green;"></i></td>
                    <td>
                        <button class="btn btn-sm btn-primary"><i class="fa-solid fa-pencil"></i></button>
                        <button class="btn btn-sm btn-danger"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                </tr>`;
        });
        tableBody_users.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});
