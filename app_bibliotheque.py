from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Auth simple
def check_auth(role):
    auth = request.authorization
    if not auth:
        return False

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (auth.username, auth.password)
    )
    user = cur.fetchone()
    conn.close()

    return user and user[0] == role

# Page d'accueil
@app.route('/')
def accueil():
    return """
    <h1>Bibliothèque</h1>
    <ul>
      <li>/livres</li>
      <li>/livre/ajouter (admin)</li>
      <li>/emprunter/ID (user)</li>
    </ul>
    """

# Voir livres disponibles
@app.route('/livres')
def livres():
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE stock > 0")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)

# Ajouter un livre (admin)
@app.route('/livre/ajouter', methods=['POST'])
def ajouter_livre():
    if not check_auth("admin"):
        return "Accès refusé", 403

    data = request.json
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (titre,auteur,stock) VALUES (?,?,?)",
        (data['titre'], data['auteur'], data['stock'])
    )
    conn.commit()
    conn.close()
    return "Livre ajouté"

# Emprunter un livre (user)
@app.route('/emprunter/<int:id>', methods=['POST'])
def emprunter(id):
    if not check_auth("user"):
        return "Accès refusé", 403

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("SELECT stock FROM books WHERE id=?", (id,))
    stock = cur.fetchone()

    if not stock or stock[0] <= 0:
        return "Livre indisponible"

    cur.execute("UPDATE books SET stock = stock - 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return "Livre emprunté"

if __name__ == "__main__":
    app.run(debug=True)
    
