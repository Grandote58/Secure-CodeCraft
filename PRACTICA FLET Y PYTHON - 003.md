# **PRACTICA FLET Y PYTHON - 003**

## Crear la misma aplicación pero con contenedores y se diferenciaran con colores con los controles ubicados de forma vertical y añadiendo la validación y sanitización de entradas. Además, se mostrará un mensaje cuando algún dato ingresado sea incorrecto, y tendrá funcionalidades de actualización y eliminación de datos utilizando checkboxes.

### Paso 1: Configuración del Proyecto

1. Instalar Python y Flet

2. Configurar un entorno virtual

3. #### Crear un proyecto básico en Flet

```python
# Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# Instalar Flet
pip install flet
```

### Paso 2: **Imports y Configuración Inicial**

```python
import flet as ft
import re
from datetime import datetime
```

### Paso 3:   Función para Sanitizar Entradas

```python
def sanitize_input(input_str, input_type):
    if input_type == "text":
        # Elimina caracteres no permitidos (solo letras y espacios)
        return re.sub(r'[^a-zA-Z\s]', '', input_str)
    elif input_type == "number":
        # Elimina caracteres no numéricos
        return re.sub(r'\D', '', input_str)
    elif input_type == "date":
        # Verifica el formato de fecha (YYYY-MM-DD)
        try:
            datetime.strptime(input_str, '%Y-%m-%d')
            return input_str
        except ValueError:
            return None
    return input_str
```

### Paso 4:**Función Principal**

```python
def main(page: ft.Page):
    page.title = "Ingreso de Datos"
```

### Paso 5: **Variables y Funciones**

- `data_list`: Lista que almacena los datos ingresados.
- `identifier`: Identificador autoincremental.
- `update_index`: Índice del elemento a actualizar.
- `add_or_update_data`: Función que agrega o actualiza datos.
- `delete_data`: Función que elimina datos seleccionados.
- `select_data_for_update`: Función que selecciona datos para actualizar.
- `update_list`: Función que actualiza la lista de datos mostrada en la interfaz.

```python
data_list = []
identifier = 1

update_index = None

def add_or_update_data(e):
    nonlocal identifier, update_index

    name = sanitize_input(txt_name.value, "text")
    id_number = sanitize_input(txt_id_number.value, "number")
    phone = sanitize_input(txt_phone.value, "number")
    birth_date = sanitize_input(txt_birth_date.value, "date")

    if not name:
        error_message.value = "Nombre incorrecto. Ejemplo: Juan Pérez"
        page.update()
        return
    if not id_number:
        error_message.value = "Número de identificación incorrecto. Ejemplo: 12345678"
        page.update()
        return
    if not phone:
        error_message.value = "Teléfono incorrecto. Ejemplo: 3001234567"
        page.update()
        return
    if not birth_date:
        error_message.value = "Fecha de nacimiento incorrecta. Ejemplo: 2000-01-01"
        page.update()
        return

    error_message.value = ""

    entry = {
        "ID": identifier,
        "Name": name,
        "ID_Number": id_number,
        "Phone": phone,
        "Birth_Date": birth_date
    }

    if update_index is not None:
        data_list[update_index] = entry
        update_index = None
        btn_add.text = "Agregar Datos"
    else:
        data_list.append(entry)
        identifier += 1

    update_list()

    txt_name.value = ""
    txt_id_number.value = ""
    txt_phone.value = ""
    txt_birth_date.value = ""
    page.update()

def delete_data(e):
    nonlocal data_list
    data_list = [entry for i, entry in enumerate(data_list) if not chk_list[i].value]
    update_list()

def select_data_for_update(e):
    nonlocal update_index
    for i, chk in enumerate(chk_list):
        if chk.value:
            entry = data_list[i]
            txt_name.value = entry["Name"]
            txt_id_number.value = entry["ID_Number"]
            txt_phone.value = entry["Phone"]
            txt_birth_date.value = entry["Birth_Date"]
            update_index = i
            btn_add.text = "Actualizar Datos"
            page.update()
            break

def update_list():
    list_view.controls.clear()
    global chk_list
    chk_list = []
    for entry in data_list:
        chk = ft.Checkbox()
        chk_list.append(chk)
        list_view.controls.append(
            ft.Row([chk, ft.Text(f"{entry['ID']}: {entry['Name']}, {entry['ID_Number']}, {entry['Phone']}, {entry['Birth_Date']}")])
        )
    page.update()
```

### Paso 6: **Campos de Entrada y Botones**

- `txt_name`, `txt_id_number`, `txt_phone`, `txt_birth_date`: Campos de entrada para los datos.
- `btn_add`: Botón que activa la función `add_or_update_data` cuando se hace clic.
- `btn_update`: Botón que selecciona datos para actualizar.
- `btn_delete`: Botón que elimina datos seleccionados.

```python
txt_name = ft.TextField(label="Nombres", width=200)
txt_id_number = ft.TextField(label="Num_Identificación", width=200)
txt_phone = ft.TextField(label="Teléfono", width=200)
txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=200)

btn_add = ft.ElevatedButton(text="Agregar Datos", on_click=add_or_update_data)
btn_update = ft.ElevatedButton(text="Seleccionar para Actualizar", on_click=select_data_for_update)
btn_delete = ft.ElevatedButton(text="Eliminar Datos", on_click=delete_data)
```

### Paso 7: **Mensaje de Error y Lista para Mostrar los Datos**

```python
error_message = ft.Text(color=ft.colors.RED)
list_view = ft.ListView(expand=True, spacing=10, padding=10)
```

### Paso 8: **Contenedores para los Controles de Entrada y Botones**

```python
input_container = ft.Container(
    content=ft.Column([txt_name, txt_id_number, txt_phone, txt_birth_date, error_message], spacing=10),
    bgcolor=ft.colors.LIGHT_BLUE_100,
    padding=20,
    border_radius=10
)

button_container = ft.Container(
    content=ft.Row([btn_add, btn_update, btn_delete], spacing=10),
    bgcolor=ft.colors.LIGHT_GREEN_100,
    padding=20,
    border_radius=10
)
```

### Paso 9: **Agregar Controles a la Página**

```python
page.add(
    input_container,
    button_container,
    list_view
)
```

### Paso 10: **Ejecutar la Aplicación**

```python
ft.app(target=main)
```

### Paso 11: Aplicación con Contenedores y Funcionalidades de Actualización y Eliminación

```python
import flet as ft
import re
from datetime import datetime

# Función para sanitizar entradas
def sanitize_input(input_str, input_type):
    if input_type == "text":
        # Elimina caracteres no permitidos (solo letras y espacios)
        return re.sub(r'[^a-zA-Z\s]', '', input_str)
    elif input_type == "number":
        # Elimina caracteres no numéricos
        return re.sub(r'\D', '', input_str)
    elif input_type == "date":
        # Verifica el formato de fecha (YYYY-MM-DD)
        try:
            datetime.strptime(input_str, '%Y-%m-%d')
            return input_str
        except ValueError:
            return None
    return input_str

# Inicialización de la aplicación
def main(page: ft.Page):
    page.title = "Ingreso de Datos"

    # Lista para almacenar los datos
    data_list = []
    identifier = 1

    # Variables para almacenar el índice del elemento a actualizar
    update_index = None

    # Función para agregar o actualizar datos al vector y a la lista
    def add_or_update_data(e):
        nonlocal identifier, update_index

        # Obtener y sanitizar los datos de los campos de entrada
        name = sanitize_input(txt_name.value, "text")
        id_number = sanitize_input(txt_id_number.value, "number")
        phone = sanitize_input(txt_phone.value, "number")
        birth_date = sanitize_input(txt_birth_date.value, "date")

        # Validar entradas
        if not name:
            error_message.value = "Nombre incorrecto. Ejemplo: Juan Pérez"
            page.update()
            return
        if not id_number:
            error_message.value = "Número de identificación incorrecto. Ejemplo: 12345678"
            page.update()
            return
        if not phone:
            error_message.value = "Teléfono incorrecto. Ejemplo: 3001234567"
            page.update()
            return
        if not birth_date:
            error_message.value = "Fecha de nacimiento incorrecta. Ejemplo: 2000-01-01"
            page.update()
            return

        # Limpiar el mensaje de error si todo está bien
        error_message.value = ""

        # Crear un diccionario con los datos
        entry = {
            "ID": identifier,
            "Name": name,
            "ID_Number": id_number,
            "Phone": phone,
            "Birth_Date": birth_date
        }

        if update_index is not None:
            # Actualizar el dato existente
            data_list[update_index] = entry
            update_index = None
            btn_add.text = "Agregar Datos"
        else:
            # Agregar el diccionario a la lista de datos
            data_list.append(entry)
            identifier += 1

        # Actualizar la lista en la interfaz de usuario
        update_list()

        # Limpiar los campos de entrada
        txt_name.value = ""
        txt_id_number.value = ""
        txt_phone.value = ""
        txt_birth_date.value = ""
        page.update()

    # Función para eliminar datos seleccionados
    def delete_data(e):
        nonlocal data_list
        data_list = [entry for i, entry in enumerate(data_list) if not chk_list[i].value]
        update_list()

    # Función para seleccionar datos para actualizar
    def select_data_for_update(e):
        nonlocal update_index
        for i, chk in enumerate(chk_list):
            if chk.value:
                entry = data_list[i]
                txt_name.value = entry["Name"]
                txt_id_number.value = entry["ID_Number"]
                txt_phone.value = entry["Phone"]
                txt_birth_date.value = entry["Birth_Date"]
                update_index = i
                btn_add.text = "Actualizar Datos"
                page.update()
                break

    # Función para actualizar la lista en la interfaz
    def update_list():
        list_view.controls.clear()
        global chk_list
        chk_list = []
        for entry in data_list:
            chk = ft.Checkbox()
            chk_list.append(chk)
            list_view.controls.append(
                ft.Row([chk, ft.Text(f"{entry['ID']}: {entry['Name']}, {entry['ID_Number']}, {entry['Phone']}, {entry['Birth_Date']}")])
            )
        page.update()

    # Campos de entrada
    txt_name = ft.TextField(label="Nombres", width=200)
    txt_id_number = ft.TextField(label="Num_Identificación", width=200)
    txt_phone = ft.TextField(label="Teléfono", width=200)
    txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=200)

    # Botones para agregar, actualizar y eliminar datos
    btn_add = ft.ElevatedButton(text="Agregar Datos", on_click=add_or_update_data)
    btn_update = ft.ElevatedButton(text="Seleccionar para Actualizar", on_click=select_data_for_update)
    btn_delete = ft.ElevatedButton(text="Eliminar Datos", on_click=delete_data)

    # Mensaje de error
    error_message = ft.Text(color=ft.colors.RED)

    # Lista para mostrar los datos
    list_view = ft.ListView(expand=True, spacing=10, padding=10)

    # Contenedores para los controles de entrada y botones
    input_container = ft.Container(
        content=ft.Column([txt_name, txt_id_number, txt_phone, txt_birth_date, error_message], spacing=10),
        bgcolor=ft.colors.LIGHT_BLUE_100,
        padding=20,
        border_radius=10
    )

    button_container = ft.Container(
        content=ft.Row([btn_add, btn_update, btn_delete], spacing=10),
        bgcolor=ft.colors.LIGHT_GREEN_100,
        padding=20,
        border_radius=10
    )

    # Agregar controles a la página de forma vertical
    page.add(
        input_container,
        button_container,
        list_view
    )

# Ejecutar la aplicación
ft.app(target=main)
```