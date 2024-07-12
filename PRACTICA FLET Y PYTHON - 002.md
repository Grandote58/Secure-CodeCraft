# **PRACTICA FLET Y PYTHON - 002**

## Crear la misma aplicación pero con los controles ubicados de forma vertical y añadiendo la validación y sanitización de entradas. Además, se mostrará un mensaje cuando algún dato ingresado sea incorrecto.

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

### Paso 2:**Imports y Configuración Inicial**

```python
import flet as ft
import re
from datetime import datetime
```

### Paso 3:**Función para Sanitizar Entradas**

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

### Paso 5:**Variables y Funciones**

- `data_list`: Lista que almacena los datos ingresados.
- `identifier`: Identificador autoincremental.
- `add_data`: Función que agrega datos a la lista y actualiza la interfaz.
- `update_list`: Función que actualiza la lista de datos mostrada en la interfaz.

```python
data_list = []
identifier = 1

def add_data(e):
    nonlocal identifier
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

    data_list.append(entry)
    identifier += 1
    update_list()

    txt_name.value = ""
    txt_id_number.value = ""
    txt_phone.value = ""
    txt_birth_date.value = ""
    page.update()

def update_list():
    list_view.controls.clear()
    for entry in data_list:
        list_view.controls.append(
            ft.Text(f"{entry['ID']}: {entry['Name']}, {entry['ID_Number']}, {entry['Phone']}, {entry['Birth_Date']}")
        )
    page.update()
```

### Paso 6:**Campos de Entrada y Botón**

- `txt_name`, `txt_id_number`, `txt_phone`, `txt_birth_date`: Campos de entrada para los datos.
- `btn_add`: Botón que activa la función `add_data` cuando se hace clic.

```python
txt_name = ft.TextField(label="Nombres", width=200)
txt_id_number = ft.TextField(label="Num_Identificación", width=200)
txt_phone = ft.TextField(label="Teléfono", width=200)
txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=200)

btn_add = ft.ElevatedButton(text="Agregar Datos", on_click=add_data)
```

### Paso 7:**Mensaje de Error y Lista para Mostrar los Datos**

```python
error_message = ft.Text(color=ft.colors.RED)
list_view = ft.ListView(expand=True, spacing=10, padding=10)
```

### Paso 8:**Agregar Controles a la Página**

```python
page.add(
    ft.Column([txt_name, txt_id_number, txt_phone, txt_birth_date, btn_add, error_message, list_view])
)
```

### Paso 9:**Ejecutar la Aplicación**

```python
ft.app(target=main)
```

### **Paso 10:Resumen Aplicación con Validación y Sanitización**

#### **main.py**

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

    # Función para agregar datos al vector y a la lista
    def add_data(e):
        nonlocal identifier
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

        # Crear un diccionario con los datos y el identificador
        entry = {
            "ID": identifier,
            "Name": name,
            "ID_Number": id_number,
            "Phone": phone,
            "Birth_Date": birth_date
        }

        # Agregar el diccionario a la lista de datos
        data_list.append(entry)

        # Incrementar el identificador para el próximo ingreso
        identifier += 1

        # Actualizar la lista en la interfaz de usuario
        update_list()

        # Limpiar los campos de entrada
        txt_name.value = ""
        txt_id_number.value = ""
        txt_phone.value = ""
        txt_birth_date.value = ""
        page.update()

    # Función para actualizar la lista en la interfaz
    def update_list():
        list_view.controls.clear()
        for entry in data_list:
            list_view.controls.append(
                ft.Text(f"{entry['ID']}: {entry['Name']}, {entry['ID_Number']}, {entry['Phone']}, {entry['Birth_Date']}")
            )
        page.update()

    # Campos de entrada
    txt_name = ft.TextField(label="Nombres", width=200)
    txt_id_number = ft.TextField(label="Num_Identificación", width=200)
    txt_phone = ft.TextField(label="Teléfono", width=200)
    txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=200)

    # Botón para agregar datos
    btn_add = ft.ElevatedButton(text="Agregar Datos", on_click=add_data)

    # Mensaje de error
    error_message = ft.Text(color=ft.colors.RED)

    # Lista para mostrar los datos
    list_view = ft.ListView(expand=True, spacing=10, padding=10)

    # Agregar controles a la página de forma vertical
    page.add(
        ft.Column([txt_name, txt_id_number, txt_phone, txt_birth_date, btn_add, error_message, list_view])
    )

# Ejecutar la aplicación
ft.app(target=main)
```