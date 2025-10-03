from presentation.Routes.route import app
from db.db import db

# Création des tables
with app.app_context():
    db.create_all()

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True, port=5000)