from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a tu base de datos local en XAMPP
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='prompts_db'  
    )
    return connection

# Ruta principal: Muestra el formulario y lista los prompts guardados
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM prompts')
    prompts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', prompts=prompts)

# Ruta para recibir los datos del formulario y guardarlos en MySQL
@app.route('/guardar', methods=['POST'])
def guardar():
    materia = request.form['materia']
    descripcion = request.form['descripcion']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prompts (materia, descripcion) VALUES (%s, %s)', (materia, descripcion))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)