from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = {'./static/file_bukti', './static/profile_pics'}

koneksi_mongodb = 'mongodb+srv://finalproject387:finalproject@cluster0.86upttf.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(koneksi_mongodb)
db = client.dbfinal_project

SECRET_KEY = 'finalProject'
TOKEN_KEY = 'mytoken'

@app.route('/')
def homeLogin():
    return render_template('home.html')

@app.route('/admin', methods=['GET'])
def home_admin():
    return render_template('profile_admin.html')

@app.route('/user', methods=['GET'])
def home_user():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        name_info = db.user.find_one({
            'name': payload.get('name')})
        return render_template('user.html', name_info=name_info)
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
        "pw": pw_hash,
        "profile_pic" : "",
        "profile_pic_real": "profile_pics/profile_placeholder.png"})
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
            algorithm="HS256"
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
        return jsonify({"result": "fail"})

@app.route('/homepage_user/pengaduan',methods=['GET'])
def pengaduan():
        name_info = db.user.find_one()
        return render_template('pengaduan.html', name_info=name_info)

@app.route('/posting',methods=['POST'])
def pengaduan_post():
        username_receive = request.form.get('username_give')
        pengaduan_receive = request.form.get('pengaduan_give')
        file_receive = request.form.get('file_give')

        if "file_give" in request.files:
            file = request.files["file_give"]
            file.save("./static/file_bukti")
        
        doc={
        "name" : username_receive,
        "pengaduan": pengaduan_receive,
        "file":file_receive}

        db.pengaduan.insert_one(doc)

        return jsonify({"result": "success"})


@app.route('/homepage_user/status',methods=['GET'])
def status():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms="HS256",
        )
        name_info = db.user.find_one({
            'name': payload.get('name')})
        return render_template('status.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/homepage_user')
    
@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')
        name = payload['name']
        name_receive = request.form["name_give"]
        
        new_doc = {
            "name": name_receive,
            }
        
        if "file_give" in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{name}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        
        db.user.update_one(
            {"nik": payload['nik']}, 
            {"$set": new_doc}
            )
        return jsonify({
            'result': 'success', 
            'msg': 'Your profile has been updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)