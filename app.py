from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisation Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///festival.db"
app.config["SECRET_KEY"] = "secret_key"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# =============================
# MODELES
# =============================

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Artiste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    style = db.Column(db.String(100))
    description = db.Column(db.Text)

class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50))
    lieu = db.Column(db.String(100))
    artiste_id = db.Column(db.Integer, db.ForeignKey("artiste.id"), nullable=False)
    artiste = db.relationship("Artiste", backref=db.backref("concerts", lazy=True))

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(100))
    email_client = db.Column(db.String(100))
    presence = db.Column(db.Boolean, default=False)
    concert_id = db.Column(db.Integer, db.ForeignKey("concert.id"), nullable=False)
    concert = db.relationship("Concert", backref=db.backref("reservations", lazy=True))


# =============================
# ENDPOINTS ADMIN
# =============================



# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)
