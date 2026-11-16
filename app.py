"""Appli locale de lineups CS2 : python app.py puis http://127.0.0.1:5000"""
import json
import os
import tempfile
import threading
import webbrowser
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DB = DATA / "lineups.json"
SCREENS = DATA / "screens"
PORT = 5000

# Champs modifiables depuis l'interface
EDITABLE = {"nom", "cible", "depuis", "lancer", "clic", "position", "visee",
            "temps_vol_s", "notes", "zone", "type", "side"}

lock = threading.Lock()
app = Flask(__name__, static_folder=str(BASE / "static"), static_url_path="")


def load_db():
    return json.loads(DB.read_text(encoding="utf-8"))


def save_db(db):
    # Écriture atomique : on écrit un fichier temporaire puis on remplace
    fd, tmp = tempfile.mkstemp(dir=DATA, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DB)


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/lineups")
def get_lineups():
    return jsonify(load_db())


@app.put("/api/lineups/<lid>")
def update_lineup(lid):
    patch = request.get_json(force=True) or {}
    with lock:
        db = load_db()
        for lineup in db["lineups"]:
            if lineup["id"] == lid:
                for key, value in patch.items():
                    if key in EDITABLE:
                        lineup[key] = value
                save_db(db)
                return jsonify(lineup)
    abort(404)


@app.get("/screens/<path:p>")
def screens(p):
    return send_from_directory(SCREENS, p)


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    app.run(host="127.0.0.1", port=PORT, debug=False)
