from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from pymongo import MongoClient
import jwt
import datetime
from datetime import datetime, timedelta
import hashlib
from werkzeug.utils import secure_filename
from bson import ObjectId
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

koneksi_mongodb = 'mongodb://finalproject387:finalproject@ac-vhmfphz-shard-00-00.86upttf.mongodb.net:27017,ac-vhmfphz-shard-00-01.86upttf.mongodb.net:27017,ac-vhmfphz-shard-00-02.86upttf.mongodb.net:27017/?ssl=true&replicaSet=atlas-wpdkgq-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(koneksi_mongodb)
db = client.dbfinal_project

SECRET_KEY = 'finalProject'
TOKEN_KEY = 'mytoken'
TOKEN_ADMIN = 'admintoken'

@app.route('/')
def homeLogin():
    return render_template('home.html')

@app.route('/admin', methods=['GET'])
def home_admin():
    token_receive = request.cookies.get(TOKEN_ADMIN)
    data_masyarakat = db.user.find()
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.admin.find_one({
            'id': payload["id"]})
        return render_template('profile_admin.html', name_info=name_info, data_masyarakat=data_masyarakat)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('loginAdmin'))

@app.route('/user', methods=['GET'])
def home_user():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
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
    longname_receive = request.form.get('longname_give')
    nik_receive = request.form.get('nik_give')
    alamat_receive = request.form.get('alamat_give')
    pw_receive = request.form.get('pw_give')

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    db.user.insert_one({
        "long_name":longname_receive,
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
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
        return render_template('pengaduan.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('loginUser'))

@app.route('/posting',methods=['POST'])
def pengaduan_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')        
        name_info = db.user.find_one({
            'name': payload["name"]})
        name = request.form.get('name')
        pengaduan = request.form.get('pengaduan')
        tanggal = request.form.get('tanggal')
        tanggal_upload = request.form['today']
        file = request.files["file"]
        
        file_path= ""
        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
            file_path = f'pengaduan-{mytime}.{extension}'
            file.save("./static/bukti/" + file_path)

        
        doc={
            "name" : name,
            "pengaduan": pengaduan,
            "tanggal_kejadian": tanggal,
            "file":file_path,
            "tanggal_upload":tanggal_upload
        }
        print(doc)
        db.pengaduan.insert_one(doc)

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route ('/download_pengaduan/<file>', methods=['GET'])
def download_pengaduan(file):
    path= "./static/bukti/"
    file_path = os.path.join(path, file)  
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    
    else:
        return 'File not found'

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

@app.route('/homepage_user/status',methods=['GET'])
def status():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
        return render_template('status.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))
    
@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')
        name = payload['name']
        longname_receive = request.form["longname_give"]
        
        new_doc = {
            "long_name": longname_receive,
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
            {"name": payload['name']}, 
            {"$set": new_doc}
            )
        return jsonify({
            'result': 'success', 
            'msg': 'Your profile has been updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route('/pelayanan/kelahiran', methods=['GET'])
def kelahiran():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
        return render_template('surat_kelahiran.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route('/pelayanan/kelahiran', methods=['POST'])
def kelahiran_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')        
        name = payload['name']
        
        name = request.form['name']
        tempat = request.form['tempat']
        tanggal = request.form['tanggal']
        ayah = request.form['ayah']
        ibu = request.form['ibu']
        no = request.form['no']
        jk = request.form['jenis-kelamin']

        file = request.files["pdf"]
        
        file_path= ""

        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f'Kelahiran-{name}.{extension}'
            file.save("./static/syarat/" + file_path)

        
        doc={
            "nama_bayi" : name,
            "tempat_lahir": tempat,
            "tanggal_lahir": tanggal,
            "ayah":ayah,
            "ibu":ibu,
            "anak-ke":no,
            "jk" : jk,
            "file":file_path,
            "status": "",
            "surat" : "",
        }
        db.kelahiran.insert_one(doc)
        return redirect('/pelayanan/kelahiran')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route('/pelayanan/domisili', methods=['GET'])
def domisili():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
        return render_template('surat_domisili.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))
    
@app.route('/pelayanan/domisili', methods=['POST'])
def domisili_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')        
        name = payload['name']
        
        name = request.form['name']
        ttl = request.form['ttl']
        jk = request.form['jenis-kelamin']
        work = request.form['work']
        alamat = request.form['alamat']

        file = request.files["pdf"]
        
        file_path= ""

        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f'Domisili-{name}.{extension}'
            file.save("./static/syarat/" + file_path)

        
        doc={
            "nama" : name,
            "ttl" : ttl,
            "work" : work,
            "alamat":alamat,
            "jk" : jk,
            "file":file_path,
            "status": "",
            "surat" : "",
        }
        db.domisili.insert_one(doc)
        return redirect('/pelayanan/domisili')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))
    
@app.route('/pelayanan/kematian', methods=['GET'])
def kematian():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        name_info = db.user.find_one({
            'name': payload["name"]})
        return render_template('surat_kematian.html', name_info=name_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

@app.route('/pelayanan/kematian', methods=['POST'])
def kematian_post():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')        
        name = payload['name']
        
        name = request.form['nama']
        ttl = request.form['ttl']
        agama = request.form['agama']
        jk = request.form['jenis-kelamin']
        tempat = request.form['tempat']
        tanggal = request.form['tanggal']
        penyebab = request.form['penyebab']

        file = request.files["pdf"]
        
        file_path= ""

        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f'Kematian-{name}.{extension}'
            file.save("./static/syarat/" + file_path)

        
        doc={
            "nama" : name,
            "ttl" : ttl,
            "agama" :agama,
            "jk" : jk,
            "tempat" : tempat,
            "tanggal": tanggal,
            "penyebab" : penyebab,
            "file":file_path,
            "status": "",
            "surat" : "",
        }
        db.kematian.insert_one(doc)
        return redirect('/pelayanan/kematian')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home_user'))

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