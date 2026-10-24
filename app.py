from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/api/login', methods=['POST'])
def login():
    req = request.json
    username = req.get('username', '').strip()
    password = req.get('password', '').strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "نام کاربری و رمز عبور الزامی است."})

    db = load_db()

    if username not in db:
        db[username] = {
            "password": password,
            "mined": 0,
            "miners": [{"name": "ماینر رایگان پایه", "hashrate": "68.4 TH/s", "maxDaily": 35000}],
            "withdrawHistory": [],
            "lastMiningTime": 0,
            "isMining": False,
            "isChannelJoined": False,
            "lastBonusTime": 0,
            "miningCrypto": "USDT"
        }
        save_db(db)
        return jsonify({"status": "success", "user": db[username], "message": "ثبت‌نام با موفقیت انجام شد."})
    
    if db[username]["password"] != password:
        return jsonify({"status": "error", "message": "رمز عبور اشتباه است!"})

    return jsonify({"status": "success", "user": db[username], "message": "ورود موفقیت‌آمیز."})

@app.route('/api/update', methods=['POST'])
def update_user():
    req = request.json
    username = req.get('username')
    userData = req.get('userData')

    if not username or not userData:
        return jsonify({"status": "error", "message": "داده نامعتبر"})

    db = load_db()
    db[username] = userData
    save_db(db)
    return jsonify({"status": "success"})

@app.route('/api/get_all', methods=['GET'])
def get_all_users():
    db = load_db()
    return jsonify(db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)