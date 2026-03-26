from flask import Flask, render_template_string, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "ma_cle_secrete"

# URL de ton backend JWT (Jour 15)
API_URL = "http://127.0.0.1:5000"

# Page de connexion
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Appel API backend pour obtenir le token
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["token"]
            session["token"] = token
            session["username"] = username
            return redirect(url_for("ventes"))
        return "Login échoué"
    return """
    <h1>Connexion</h1>
    <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Se connecter</button>
    </form>
    """

# Page affichant les ventes
@app.route("/ventes")
def ventes():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/api/ventes", headers=headers)
    if response.status_code == 200:
        ventes = response.json()
        html = """
        <h1>Liste des ventes</h1>
        <p>Connecté en tant que {{username}}</p>
        <table border=1>
            <tr><th>ID</th><th>Produit</th><th>Prix</th><th>Quantité</th><th>Date</th><th>Revenu</th></tr>
            {% for v in ventes %}
            <tr>
                <td>{{v.id}}</td>
                <td>{{v.produit}}</td>
                <td>{{v.prix}}</td>
                <td>{{v.quantite}}</td>
                <td>{{v.date}}</td>
                <td>{{v.revenu}}</td>
            </tr>
            {% endfor %}
        </table>
        <a href='/logout'>Se déconnecter</a>
        """
        return render_template_string(html, ventes=ventes, username=session.get("username"))
    return "Erreur lors de la récupération des ventes"

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=5001, debug=True)
