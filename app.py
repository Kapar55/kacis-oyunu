from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SCORE_FILE = "score.json"

# skor dosyası yoksa oluştur
if not os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "w") as f:
        json.dump({"name": "Yok", "score": 0}, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_score")
def get_score():
    try:
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"name": "Yok", "score": 0})

@app.route("/set_score", methods=["POST"])
def set_score():
    data = request.get_json()

    name = data.get("name", "Anon")
    score = data.get("score", 0)

    try:
        with open(SCORE_FILE, "r") as f:
            best = json.load(f)
    except:
        best = {"name": "Yok", "score": 0}

    if score > best["score"]:
        best = {"name": name, "score": score}
        with open(SCORE_FILE, "w") as f:
            json.dump(best, f)

    return jsonify(best)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
