from pymongo import MongoClient 
import jwt 
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template,jsonify,request,redirect,url_for
from werkzeug.utils import secure_filename 

MONGODB_CONNECTION_STRING = "mongodb+srv://jaul:kelompok4@cluster0.iyckasz.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "umkm"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]


app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

    
@app.route('/transaksi_user')
def transaksi_user():
    id_receive = request.form.get('id_give')
    hasils = list(db.catalog.find_one({'_id': id_receive}))
    users = list(db.user.find_one({}, {'_id': False}))
    return render_template('transaksi_user.html', hasils=hasils, users=users)

@app.route("/catalog_user", methods=["GET"])
def catalog_user():
    cat_list = list(db.catalog.find({}))
    return jsonify({'catalog': cat_list})


@app.route("/upload_bukti", methods=["GET"])
def upload_bukti():
    return render_template('upload_bukti.html')

@app.route("/riwayat_order", methods=["GET"])
def riwayat_order():
    transaksi = list(db.transaksi.find({}))
    return render_template('riwayat_order.html', transaksi=transaksi)

@app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template('signup_user.html')

@app.route('/sign_up/save', methods=['POST'])
def signup_save():
    username_receive = request.form.get('username_give')
    password_receive = request.form.get('password_give')
    nama_receive = request.form.get('nama_give')
    email_receive = request.form.get('email_give')
    pass2_receive = request.form.get('pass2_give')
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "nama": nama_receive,
        "username": username_receive,                               
        "password": password_hash,                                  
        "email": email_receive,   
        "pass2": pass2_receive,                                      
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})



@app.route("/login")
def login():
    return render_template('login_user.html')

@app.route("/admin_cat")
def admin_cat():
    catalogs = db.catalog.find()
    return render_template('admin_cat.html', catalogs=catalogs)


@app.route("/input_cat")
def input_cat():
    return render_template("input_cat.html")

@app.route("/input", methods=["POST"])
def input():
        brand_receive = request.form["brand_give"]
        ukuran_receive = request.form["ukuran_give"]
        harga_receive = request.form["harga_give"]
        deskripsi_receive = request.form["deskripsi_give"]
        image_give = request.form["image_give"]
        doc = {
        "brand" : brand_receive,
        "ukuran": ukuran_receive,
        "harga": harga_receive,
        "deskripsi": deskripsi_receive,
        "image": image_give,
        }
        db.catalog.insert_one(doc)
        return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)