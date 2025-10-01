from flask import Flask, render_template_string

app = Flask(__name__)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask App</title>
    </head>
    <body>
        <h1>Bienvenue dans ton app Flask 🎉</h1>
        <p>Ceci est la page d'accueil.</p>
        <a href="/about">À propos</a>
    </body>
    </html>
    """)

@app.route("/about")
def about():
    return "<h2>À propos : Ceci est une application Flask de base.</h2>"

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
