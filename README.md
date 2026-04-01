# FestyShow
from flask import Flask, jsonify
def create_app() -> Flask:
    app = Flask(__name__)
    .get("/")
    def hello_world():
        return jsonify({"message": "hello world - Flask API 1"}), 200
    u/app.get("/health")
    def health_check():
        return jsonify({"status": "ok"}), 200
    return app
app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=False)
