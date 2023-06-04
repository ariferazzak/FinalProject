from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
koneksi_mongodb = 'mongodb://razzak:razzak08@ac-klaldor-shard-00-00.eeumlbk.mongodb.net:27017,ac-klaldor-shard-00-01.eeumlbk.mongodb.net:27017,ac-klaldor-shard-00-02.eeumlbk.mongodb.net:27017/?ssl=true&replicaSet=atlas-7byu10-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(koneksi_mongodb)
db = client.dbfinal_project

SECRET_KEY = 'finalProject'

@app.route('/')
def homeLogin():
    return render_template('home.html')

@app.route('/login/admin')
def loginAdmin():
    return render_template('login_admin.html')

@app.route('/login/user')
def loginUser():
    return render_template('login_user.html')

@app.route('/register/admin')
def registerAdmin():
    return render_template('register_admin.html')

@app.route('/register/user')
def registerUser():
    return render_template('register_user.html')

# api register sisi admin
@app.route('/api/register/admin', methods=['POST'])
def api_register_admin():
    id_receive = request.form.get('id_give')
    username_receive = request.form.get('username_give')
    pw_receive = request.form.get('pw_give')

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    db.user.insert_one({
        "id": id_receive, 
        "pw": pw_hash, 
        "name": username_receive})

    return jsonify({"result": "success"})

# api register sisi user
@app.route('/api/register/user', methods=['POST'])
def api_register_user():
    username_receive = request.form.get('username_give')
    nik_receive = request.form.get('nik_give')
    alamat_receive = request.form.get('alamat_give')
    pw_receive = request.form.get('pw_give')

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    db.user.insert_one({
        "name": username_receive, 
        "nik": nik_receive,
        "alamat": alamat_receive,
        "pw": pw_hash,})
    return jsonify({"result": "success"})

# api login sisi admin
@app.route('/api/login/admin', methods=['POST'])
def api_login_admin():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({
        "id": id_receive, 
        "pw": pw_hash
        })
    if result is not None:
        payload ={
            "id": id_receive,
            "exp": datetime.utcnow() + timedelta(seconds=5),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
            )
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})
    
# api login sisi user
@app.route('/api/login/user', methods=['POST'])
def api_login_user():
    username_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({
        "name": username_receive, 
        "pw": pw_hash
        })
    if result is not None:
        payload ={
            "name": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=5),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
            )
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)