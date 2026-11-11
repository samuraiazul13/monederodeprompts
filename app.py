import os
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

app = Flask(__name__)


# Configuración dinámica para XAMPP (local) o Render/Aiven (nube)
def get_db_connection():
  return mysql.connector.connect(
      host=os.environ.get("DB_HOST", "localhost"),
      user=os.environ.get("DB_USER", "root"),
      password=os.environ.get("DB_PASSWORD", ""),
      database=os.environ.get("DB_NAME", "prompts_db"),
      port=int(os.environ.get("DB_PORT", 3306)),
  )


# Función para crear la tabla automáticamente si no existe
def init_db():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                materia VARCHAR(100) NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabla 'prompts' verificada/creada exitosamente.")
  except Exception as e:
    print(f"Error al crear la tabla: {e}")


# Ejecutar la verificación al arrancar la app
init_db()


# Ruta principal: Muestra el formulario y lista los prompts guardados
@app.route("/")
def index():
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM prompts")
  prompts = cursor.fetchall()
  cursor.close()
  conn.close()
  return render_template("index.html", prompts=prompts)


# Ruta para recibir los datos del formulario y guardarlos en MySQL
@app.route("/guardar", methods=["POST"])
def guardar():
  materia = request.form["materia"]
  descripcion = request.form["descripcion"]

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO prompts (materia, descripcion) VALUES (%s, %s)",
      (materia, descripcion),
  )
  conn.commit()
  cursor.close()
  conn.close()

  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True, port=5000)