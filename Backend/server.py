from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

DB_NAME = "notas.db"

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/notas', methods=['GET'])
def get_notas():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, titulo, contenido FROM notas")
    notas = [{"id": row[0], "titulo": row[1], "contenido": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(notas)

@app.route('/notas', methods=['POST'])
def agregar_nota():
    data = request.get_json()
    titulo = data.get("titulo")
    contenido = data.get("contenido")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO notas (titulo, contenido) VALUES (?, ?)", (titulo, contenido))
    conn.commit()
    conn.close()
    return jsonify({"message": "Nota agregada"}), 201

# Servir frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
