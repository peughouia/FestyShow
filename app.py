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

@app.route("/admin/register", methods=["POST"])
def register_admin():
    data = request.json
    if Admin.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Admin déjà existant"}), 400
    
    admin = Admin(username=data["username"])
    admin.set_password(data["password"])
    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin créé"}), 201

@app.route("/admin/login", methods=["POST"])
def login_admin():
    data = request.json
    admin = Admin.query.filter_by(username=data["username"]).first()
    if admin and admin.check_password(data["password"]):
        return jsonify({"message": "Connexion réussie"}), 200
    return jsonify({"message": "Identifiants invalides"}), 401

# =============================
# ENDPOINTS ARTISTES
# =============================

@app.route("/artistes", methods=["POST"])
def create_artiste():
    data = request.json
    artiste = Artiste(nom=data["nom"], style=data.get("style"), description=data.get("description"))
    db.session.add(artiste)
    db.session.commit()
    return jsonify({"message": "Artiste créé"}), 201

@app.route("/artistes", methods=["GET"])
def get_artistes():
    artistes = Artiste.query.all()
    return jsonify([{"id": a.id, "nom": a.nom, "style": a.style} for a in artistes])


# =============================
# ENDPOINTS CONCERTS
# =============================

@app.route("/concerts", methods=["POST"])
def create_concert():
    data = request.json
    if not Artiste.query.get(data["artiste_id"]):
        return jsonify({"message": "Artiste introuvable"}), 404
    
    concert = Concert(
        titre=data["titre"],
        date=data.get("date"),
        lieu=data.get("lieu"),
        artiste_id=data["artiste_id"]
    )
    db.session.add(concert)
    db.session.commit()
    return jsonify({"message": "Concert créé"}), 201

@app.route("/concerts", methods=["GET"])
def get_concerts():
    concerts = Concert.query.all()
    return jsonify([
        {"id": c.id, "titre": c.titre, "date": c.date, "lieu": c.lieu, "artiste": c.artiste.nom}
        for c in concerts
    ])


# =============================
# ENDPOINTS RESERVATIONS
# =============================

@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.json
    if not Concert.query.get(data["concert_id"]):
        return jsonify({"message": "Concert introuvable"}), 404
    
    reservation = Reservation(
        nom_client=data["nom_client"],
        email_client=data["email_client"],
        concert_id=data["concert_id"]
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Réservation créée"}), 201

@app.route("/reservations/concert/<int:concert_id>", methods=["GET"])
def get_reservations(concert_id):
    reservations = Reservation.query.filter_by(concert_id=concert_id).all()
    return jsonify([
        {"id": r.id, "nom_client": r.nom_client, "email_client": r.email_client, "presence": r.presence}
        for r in reservations
    ])


# =============================
# ENDPOINTS STATISTIQUES
# =============================

@app.route("/stats/concert/<int:concert_id>", methods=["GET"])
def stats_concert(concert_id):
    concert = Concert.query.get(concert_id)
    if not concert:
        return jsonify({"message": "Concert introuvable"}), 404
    
    total = Reservation.query.filter_by(concert_id=concert_id).count()
    participants = Reservation.query.filter_by(concert_id=concert_id, presence=True).count()
    
    return jsonify({
        "concert": concert.titre,
        "total_reservations": total,
        "participants": participants,
        "taux_participation": f"{(participants/total*100) if total > 0 else 0:.2f}%"
    })

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)
