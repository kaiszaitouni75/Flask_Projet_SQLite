from flask import Flask, render_template, request, redirect, url_for, session, Response
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key_projet"

# =====================================================
# FONCTIONS UTILITAIRES
# =====================================================

def est_authentifie():
    return session.get('authentifie')

# =====================================================
# ACCUEIL
# =====================================================

@app.route('/')
def hello_world():
    return render_template('hello.html')

# =====================================================
# AUTHENTIFICATION
# =====================================================

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session['authentifie'] = True
            session['username'] = user[1]
            session['role'] = user[2]
            session['user_id'] = user[0]
            return redirect(url_for('liste_livres'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# =====================================================
# GESTION DES LIVRES
# =====================================================

@app.route('/livres/')
def liste_livres():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()

    return render_template('livres.html', livres=livres)


@app.route('/livres/ajouter', methods=['GET', 'POST'])
def ajouter_livre():
    if not est_authentifie() or session.get('role') != 'admin':
        return "<h3>Accès refusé : admin uniquement</h3>"

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        stock = int(request.form['stock'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)',
            (titre, auteur, stock)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('liste_livres'))

    return render_template('ajouter_livre.html')


@app.route('/livres/supprimer/<int:livre_id>', methods=['POST'])
def supprimer_livre(livre_id):
    if session.get('role') != 'admin':
        return "<h3>Accès refusé : admin uniquement</h3>"

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (livre_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('liste_livres'))

# =====================================================
# GESTION DES TÂCHES
# =====================================================

@app.route('/taches/')
def liste_taches():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
    tasks = cursor.fetchall()
    conn.close()

    return render_template('taches.html', tasks=tasks)


@app.route('/taches/ajouter', methods=['GET', 'POST'])
def ajouter_tache():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
            (title, description, due_date)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('liste_taches'))

    return render_template('ajouter_tache.html')


@app.route('/taches/supprimer/<int:id>')
def supprimer_tache(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('liste_taches'))


@app.route('/taches/terminer/<int:id>')
def terminer_tache(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('liste_taches'))

# =====================================================
# LANCEMENT
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
