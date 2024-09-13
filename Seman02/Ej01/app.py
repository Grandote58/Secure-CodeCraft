from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos
def get_db_connection():
    conn = sqlite3.connect('compras.db')
    conn.row_factory = sqlite3.Row  # Retorna las filas como diccionarios
    return conn


# Ruta para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el archivo HTML



# Ruta para obtener todos los clientes
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn = get_db_connection()
        customers = conn.execute('SELECT * FROM customers').fetchall()
        conn.close()

        if not customers:
            return jsonify({"message": "No se encontraron clientes"}), 404

        return jsonify([dict(customer) for customer in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un cliente por ID
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        conn = get_db_connection()
        customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
        conn.close()

        if customer is None:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify(dict(customer)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para agregar un cliente
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()

        # Validación de los datos
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')

        if not nombre or not email:
            return jsonify({"error": "Nombre y email son obligatorios"}), 400

        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
                (nombre, email, telefono)
            )
            conn.commit()

        return jsonify({"message": "Cliente agregado correctamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un cliente
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        data = request.get_json()

        # Validación de los datos
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')

        if not nombre or not email:
            return jsonify({"error": "Nombre y email son obligatorios"}), 400

        with get_db_connection() as conn:
            result = conn.execute(
                'UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?',
                (nombre, email, telefono, id)
            )
            conn.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente actualizado correctamente"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un cliente
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        with get_db_connection() as conn:
            result = conn.execute('DELETE FROM customers WHERE id = ?', (id,))
            conn.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
