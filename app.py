from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
koneksi_mongodb = 'mongodb://test:sparta@ac-rlfmp5k-shard-00-00.waymkxr.mongodb.net:27017,ac-rlfmp5k-shard-00-01.waymkxr.mongodb.net:27017,ac-rlfmp5k-shard-00-02.waymkxr.mongodb.net:27017/?ssl=true&replicaSet=atlas-yzrfcr-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(koneksi_mongodb)
db = client.dbfinal_project

SECRET_KEY = 'finalProject'
TOKEN_KEY = 'mytoken'

@app.route('/')
def homeLogin():
    return render_template('home.html')

@app.route('/homepage_admin', methods=['GET'])
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
            )
        admin_info = db.admin.find_one({'username': payload.get('id')})
        return render_template('admin.html', admin_info=admin_info)
    except jwt.ExpiredSignatureError:
        msg='Your token has expired'
        return redirect(url_for('loginAdmin', msg=msg))
    except jwt.exceptions.DecodeError:
        msg='There was problem logging you in'
        return redirect(url_for('loginAdmin', msg=msg))
    
@app.route('/homepage_user', methods=['GET'])
def home_user():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        name_info = db.user.find_one({
            'name': payload['id']})
        return render_template('user.html', name_info=name_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('loginUser'))

@app.route('/login/admin')
def loginAdmin():
    msg = request.args.get('msg')
    return render_template('login_admin.html', msg=msg)

@app.route('/login/user')
def loginUser():
    msg = request.args.get('msg')
    return render_template('login_user.html', msg=msg)

# api register sisi admin
@app.route('/register/admin', methods=['POST'])
def register_admin():
    id_receive = request.form.get('id_give')
    username_receive = request.form.get('username_give')
    alamat_receive = request.form.get('alamat_give')
    pw_receive = request.form.get('pw_give')

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    db.admin.insert_one({
        "id": id_receive,  
        "name": username_receive,
        "alamat": alamat_receive,
        "pw": pw_hash,})

    return jsonify({"result": "success"})

# api register sisi user
@app.route('/register/user', methods=['POST'])
def register_user():
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
@app.route('/login/admin', methods=['POST'])
def login_admin():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.admin.find_one({
        "id": id_receive, 
        "pw": pw_hash
        })
    if result is not None:
        payload ={
            "id": id_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=["HS256"]
            )
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})
    
# api login sisi user
@app.route('/login/user', methods=['POST'])
def login_user():
    username_receive = request.form["username_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({
        "name": username_receive, 
        "pw": pw_hash
        })
    if result is not None:
        payload ={
            "name": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
            )
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})

@app.route('/pengaduan',methods=['GET'])
def pengaduan(name):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        status = name == payload.get('nik')
        name_info = db.user.find_one({
            'name': name},
            {'_id': False})
        return render_template('status.html', name_info=name_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/homepage_user')

@app.route('/status',methods=['GET'])
def status(name):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        status = name == payload.get('nik')
        name_info = db.user.find_one({
            'name': name},
            {'_id': False})
        return render_template('status.html', name_info=name_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/homepage_user')

@app.route('/profile/admin',methods=['GET'])
def profile_admin(name):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        status = name == payload.get('nik')
        name_info = db.admin.find_one({
            'name': name},
            {'_id': False})
        return render_template('status.html', name_info=name_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/homepage_admin')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)