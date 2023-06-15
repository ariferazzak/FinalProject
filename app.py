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
    data_masyarakat = db.user.find()
    return render_template(
        'profile_admin.html',
         data_masyarakat = data_masyarakat,
        )

@app.route('/user', methods=['GET'])
def home_user():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithm="HS256",
        )
        name_info = db.user.find_one({
            'name': payload.get ('name')})
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

@app.route('/pengaduan/<username>',methods=['GET'])
def pengaduan(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithm="HS256",
        )
        username = payload.get("name")
        name_info = db.user.find_one({
            'name': username})
        return render_template('pengaduan.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user', username=username))
    
@app.route('/posting',methods=['POST'])
def pengaduan_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithm='HS256')
        name = payload['name']
        username_receive = request.form.get('username_give')
        pengaduan_receive = request.form.get('pengaduan_give')
        file_path =''
        kejadian_receive = request.form.get('kejadian_give')
        date_receive = request.form['date_give']
        file = request.files["file_give"]

        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"bukti-{name}.{extension}"
            file.save("./static/file_bukti/" + file_path)
        
        doc={
        "name" : username_receive,
        "pengaduan": pengaduan_receive,
        "tanggal_kejadian": kejadian_receive,
        "file":file_path,
        "date":date_receive}

        db.pengaduan.insert_one(doc)

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))
    
@app.route ('/posting/pengaduan', methods=['GET'])
def pengaduan_get():
    username_receive = request.args.get('username_give')
    if username_receive == '':
        posts = list(db.pengaduan.find({}).sort('date', -1).limit(20))
    else:
        posts = list(
                db.pengaduan.find({'username': username_receive}).sort('date', -1).limit(20)
            )
    for post in posts:
        post['_id'] = str(post['_id'])
    return jsonify({
            'result': 'success', 
            'msg': 'Successful fetched all posts',
            'posts': posts})

@app.route('/status/<username>',methods=['GET'])
def status(username):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithm="HS256",
        )
        status = username == payload.get ('name')
        name_info = db.user.find_one({
            'name': username})
        return render_template('status.html', name_info=name_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))
    
@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithm='HS256')
        name = payload['name']
        name_receive = request.form["name_give"]
        id = request.form["id"]
        file_path= ""
        file = request.files["file_give"]

        if file:            
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{name}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        
        new_doc = {
            "name": name_receive,
            }
        db.user.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": new_doc}
            )
        return jsonify({
            'result': 'success', 
            'msg': 'Your profile has been updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route('/pelayanan/kelahiran', methods=['GET'])
def kelahiran():
    name_info = db.user.find_one()
    return render_template('surat_kelahiran.html', name_info=name_info)

@app.route('/resume/kelahiran',methods=['GET','POST'])
def resume_kelahiran():
    return render_template('resume_kelahiran.html')

@app.route('/resume/domisili',methods=['GET','POST'])
def resume_domisili():
    return render_template('resume_domisili.html')

@app.route('/resume/kematian',methods=['GET','POST'])
def resume_kematian():
    return render_template('resume_kematian.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)