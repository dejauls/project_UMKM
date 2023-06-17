from pymongo import MongoClient 
import jwt 
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template,jsonify,request,redirect,url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config ['TEMPLATES_AUTO_RELOAD'] = True
app.config ['UPLOAD_FOLDER'] = './static/profile_pics'

MONGODB_CONNECTION_STRING = 'mongodb://jaul:kelompok4@ac-tckcnrv-shard-00-00.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-01.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-02.iyckasz.mongodb.net:27017/?ssl=true&replicaSet=atlas-ehh9a0-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.umkm

ADMIN_EMAIL = 'admin@triplesbranded.com'
ADMIN_PASSWORD = 'admin'
TOKEN_KEY = 'mytoken'
SECRET_KEY = 'SAYA'

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')
    
    
    
@app.route('/login',methods=['GET'])
def login():
    token_receive = request.cookies.get(TOKEN_KEY)
    try : 
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"username": payload["username"]})
        return render_template('home.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        msg = 'You token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'There was a promblem logging you in'
        return redirect(url_for('login', msg=msg))   

@app.route('/catalog')
def catalog():
    return render_template('cat_user.html')

@app.route('/admin/login', methods=['POST'])
def login_admin():
    email = request.form.get("inputEmail")
    password = request.form.get("inputPassword")
    doc = {
        'inputEmail' : email,
        'inputPassword' : password
    }
    db.admin.find_one(doc)
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return redirect('/admin/catalog', message='Berhasil Login!')
    else:
        return render_template('login_admin.html', error_message='Email atau password salah!')


@app.route('/admin')
def admin():
    return render_template('login_admin.html')

@app.route("/admin/catalog")
def admin_cat():
    catalogs = db.catalog.find()
    return render_template('admin_cat.html', catalogs=catalogs)


@app.route("/input_cat")
def input_cat():
    return render_template("input_cat.html")

@app.route("/inputkatalog", methods=["POST"])
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



@app.route('/admin/daftar_user')
def user():
    collection = db.users
    users = collection.find({})
   
    return render_template('daftar_user.html',
                            users=users
                            )

@app.route('/admin/list_order')
def orderan():
    collection = db['orders']
    orders = collection.find()
    return render_template('transaksi_admin.html', orders=orders)


@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "Username atau password kamu tidak ditemukan!",
            }
        )

@app.route("/sign_up")
def sign_up():
    return render_template('signup_user.html')

@app.route('/sign_up/save', methods=['POST'])
def signup_save():
    username_receive = request.form.get('username_give')
    password_receive = request.form.get('password_give')
    nama_receive = request.form.get('nama_give')
    email_receive = request.form.get('email_give')
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "nama": nama_receive,
        "username": username_receive,                               
        "password": password_hash,                                  
        "email": email_receive,                                         
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})



# untuk page input katalog
            #def insert_katalog(jenis, ukuran, harga, deskripsi):
                #db = connect_mongodb()
                #collection = db['katalog'] 
                #katalog = {
                    #'jenis': jenis,
                    #'ukuran': ukuran,
                    #'harga': harga,
                    #'deskripsi': deskripsi
                #}
                #collection.insert_one(katalog)

            # Route untuk halaman edit katalog
            #@app.route('/editkatalog', methods=['GET', 'POST'])
            #def edit_katalog():
                #if request.method == 'POST':
                    #jenis = request.form.get('jenis')
                    #ukuran = request.form.get('ukuran')
                    #harga = request.form.get('harga')
                    #deskripsi = request.form.get('deskripsi')
                    #insert_katalog(jenis, ukuran, harga, deskripsi)
                   #return 'Data berhasil disimpan ke MongoDB!'
                #return render_template('editkatalog.html')

#untuk pages edit katalog
        #def get_katalog():
            #db = connect_mongodb()
            #collection = db['katalog']  
            #katalog = collection.find()
            #return katalog

        # Fungsi untuk mengupdate data katalog 
        #def update_katalog(jenis, ukuran, harga, deskripsi):
            #db = connect_mongodb()
            #collection = db['katalog']  
            #collection.update_one(
                #{'jenis': jenis},
                #{'$set': {'ukuran': ukuran, 'harga': harga, 'deskripsi': deskripsi}}
            #)

        # Route untuk halaman edit katalog
        #@app.route('/editkatalog', methods=['GET', 'POST'])
        #def edit_katalog():
            #if request.method == 'POST':
                #jenis = request.form.get('jenis')
                #ukuran = request.form.get('ukuran')
                #harga = request.form.get('harga')
                #deskripsi = request.form.get('deskripsi')
                #update_katalog(jenis, ukuran, harga, deskripsi)
                #return 'Data berhasil diupdate di MongoDB!'
            #else:
                #katalog = get_katalog()
                #return render_template('editkatalog.html', katalog=katalog)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
