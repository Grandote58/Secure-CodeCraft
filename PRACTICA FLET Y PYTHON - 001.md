

# **PRACTICA FLET Y PYTHON - 001**

## Crear una aplicación de ingreso de datos utilizando Flet y Python, donde se almacenarán los datos en un vector y se presentarán en una lista.



### Paso 1: Configuración del Proyecto

1. Instalar Python y Flet
2. Configurar un entorno virtual
3. Crear un proyecto básico en Flet

```bash
bashCopiar código # Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# Instalar Flet
pip install flet
```

### Paso 2: **Imports y Configuración Inicial**

```python
import flet as ft
from datetime import date
```

### Paso 3:**Función Principal**

```python
def main(page: ft.Page):
    page.title = "Ingreso de Datos"
```

### Paso 4:**Variables y Funciones**

- `data_list`: Lista que almacena los datos ingresados.
- `identifier`: Identificador autoincremental.
- `add_data`: Función que agrega datos a la lista y actualiza la interfaz.
- `update_list`: Función que actualiza la lista de datos mostrada en la interfaz.

```python
pythonCopiar códigodata_list = []
identifier = 1

def add_data(e):
    nonlocal identifier
    name = txt_name.value
    id_number = txt_id_number.value
    phone = txt_phone.value
    birth_date = txt_birth_date.value
    
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

### Paso 5:**Campos de Entrada y Botón**

- `txt_name`, `txt_id_number`, `txt_phone`, `txt_birth_date`: Campos de entrada para los datos.
- `btn_add`: Botón que activa la función `add_data` cuando se hace clic.

```python
txt_name = ft.TextField(label="Nombres", width=200)
txt_id_number = ft.TextField(label="Num_Identificación", width=200)
txt_phone = ft.TextField(label="Teléfono", width=200)
txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=200)

btn_add = ft.ElevatedButton(text="Agregar Datos", on_click=add_data)
```

### Paso 6:**Lista para Mostrar los Datos**

```python
list_view = ft.ListView(expand=True, spacing=10, padding=10)
```

### Paso 7:**Agregar Controles a la Página**

```python
page.add(
    ft.Row([txt_name, txt_id_number, txt_phone, txt_birth_date, btn_add]),
    list_view
)
```

### Paso 8:**Ejecutar la Aplicación**

```python
ft.app(target=main)
```

### Paso 9: Aplicación Básica Completa

#### **main.py**

```python
import flet as ft
from datetime import date

# Inicialización de la aplicación
def main(page: ft.Page):
    page.title = "Ingreso de Datos"
    
    # Lista para almacenar los datos
    data_list = []
    identifier = 1
    
    # Función para agregar datos al vector y a la lista
    def add_data(e):
        nonlocal identifier
        # Obtener los datos de los campos de entrada
        name = txt_name.value
        id_number = txt_id_number.value
        phone = txt_phone.value
        birth_date = txt_birth_date.value
        
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
    
    # Lista para mostrar los datos
    list_view = ft.ListView(expand=True, spacing=10, padding=10)
    
    # Agregar controles a la página
    page.add(
        ft.Row([txt_name, txt_id_number, txt_phone, txt_birth_date, btn_add]),
        list_view
    )

# Ejecutar la aplicación
ft.app(target=main)
```