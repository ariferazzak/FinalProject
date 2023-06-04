from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import jwt
from datetime import datetime
import hashlib

app = Flask(__name__)
koneksi_mongodb = 'mongodb://razzak:razzak08@ac-klaldor-shard-00-00.eeumlbk.mongodb.net:27017,ac-klaldor-shard-00-01.eeumlbk.mongodb.net:27017,ac-klaldor-shard-00-02.eeumlbk.mongodb.net:27017/?ssl=true&replicaSet=atlas-7byu10-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(koneksi_mongodb)
db = client.dbfinal_project

SECRET_KEY = 'finalProject'

@app.route('/')
def homeLogin():
    return render_template('home.html')

@app.route('/login/Admin')
def loginAdmin():
    return render_template('login_admin.html')

@app.route('/login/User')
def loginUser():
    return render_template('login_user.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)