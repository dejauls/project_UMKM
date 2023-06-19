from pymongo import MongoClient 
import jwt 
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template,jsonify,request,redirect,url_for
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)

app.config ['TEMPLATES_AUTO_RELOAD'] = True
app.config ['UPLOAD_FOLDER'] = './static/profile_pics'

MONGODB_CONNECTION_STRING = 'mongodb://jaul:kelompok4@ac-tckcnrv-shard-00-00.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-01.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-02.iyckasz.mongodb.net:27017/?ssl=true&replicaSet=atlas-ehh9a0-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.umkm

TOKEN_KEY = 'mytoken'
SECRET_KEY = 'SAYA'
ADMIN_KEY = 'admintoken'

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    return render_template('cat_user.html')

@app.route('/admin')
def admin():
    return render_template('login_admin.html')

@app.route("/login")
def login():
    return render_template('login_user.html')

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

@app.route("/admin/login", methods=["POST"])
def admin_login():
    email_receive = request.form["email_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(pw_hash)
    result = db.admin.find_one(
        {
            "email": email_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": email_receive,
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
    nohp_receive = request.form.get('nomorhp_give')
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "nama": nama_receive,
        "username": username_receive,                               
        "password": password_hash,                                  
        "email": email_receive,
        "nohp":nohp_receive                                         
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


#punya rangga
@app.route("/admin_cat")
def admin_cat():
    token_receive = request.cookies.get(ADMIN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        catalog = list(db.catalog.find({}))
        for cat in catalog:
            cat['_id'] = str(cat['_id'])
        name_info = db.admin.find_one({
            'id': payload["id"]})
        return render_template('admin_cat.html', name_info=name_info, catalog=catalog)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login'))
    

@app.route("/input_cat")
def input_cat():

    return render_template("input_cat.html")
    

@app.route("/input", methods=["POST"])
def input():
    brand_receive = request.form.get('brand_give')
    ukuran_receive = request.form.get('ukuran_give')
    harga_receive = request.form.get('harga_give')
    deskripsi_receive = request.form.get('deskripsi_give')
    
    file_path= ""
    file = request.files["image_give"]
    
    filename = secure_filename(file.filename)
    extension = filename.split(".")[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    file_path = f'catalog-{mytime}.{extension}'
    file.save("./static/coba/" + file_path)

    doc = {
        'brand' : brand_receive,
        'ukuran' : ukuran_receive,
        'harga' : harga_receive,
        'deskripsi' : deskripsi_receive,
        "image": file_path
    }
    db.catalog.insert_one(doc)
    return jsonify({'msg': 'Data berhasil disimpan!'})
    
@app.route("/edit_cat", methods=['GET', 'POST'])
def edit_cat():
    if request.method == "GET":
        id = request.args.get("id")
        data = db.catalog.find_one({"_id":ObjectId(id)})
        data["_id"] = str(data["_id"])
        print(data)
        return render_template("edit_cat.html", data=data)
    
    catalog = request.form["id"]
    brand_receive = request.form["brand"]
    ukuran_receive = request.form["ukuran"]
    harga_receive = request.form["harga"]
    deskripsi_receive = request.form["deskripsi"]
    file_path= ""
    file = request.files["image"]
    
    if file:
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        file_path = f'catalog-{mytime}.{extension}'
        file.save("./static/coba/" + file_path)
    doc = {
            "brand": brand_receive,
            "ukuran": ukuran_receive,
            "harga": harga_receive,
            "deskripsi": deskripsi_receive,
            "image": file_path
        }
    db.catalog.update_one({"_id":  ObjectId(catalog)}, {"$set": doc})
    return redirect('/admin_cat')

@app.route("/detail-orderan")
def detail():
    collection = db.transaksi
    transaksi = list(collection.find())
    return render_template("detail_order.html", transaksi=transaksi)

@app.route("/update_document/<string:id>", methods=['POST'])
def update_document(id):
    new_status = request.form.get('status')

    collection = db.transaksi
    collection.update_one({'_id': id}, {'$set': {'status': new_status}})
    
    return redirect('/detail-orderan')

@app.route('/order',methods=['GET','POST'])
def order():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        print(payload)
        name_info = db.users.find_one({
            'username': payload["id"]})
        print(name_info)
        id = request.form['id']
        detail = db.catalog.find_one({'_id':ObjectId(id)})
        detail['_id'] = str(detail['_id'])
        tanggal_sekarang = datetime.now()
        tanggal = tanggal_sekarang.strftime('%d-%m-%Y')
        return render_template('transaksi_user.html', name_info=name_info, detail=detail, tanggal=tanggal)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login'))
    

@app.route('/pesan', methods=["POST"])
def pesan():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        print(payload)
        totalBelanja = request.form['totalBelanja']
        status = request.form['status']
        doc = {
            "image":request.form['image'],
            "brand":request.form['brand'],
            "harga":request.form['harga'],
            "totalBelanja":request.form['totalBelanja'],
            "nama":request.form['nama'],
            "alamat":request.form['alamat'],
            "nohp":request.form['nohp'],
            "tanggal":request.form['tanggal'],
            "status":request.form['status'],   
        }
        db.transaksi.insert_one(doc)
        return render_template('upload_bukti.html', totalBelanja = totalBelanja, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login'))



@app.route("/upload_bukti", methods=["POST"])
def upload_bukti():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        print(payload)
        file_path= ""
        file = request.files["image"]
        
        if file:
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
            file_path = f'bukti-{mytime}.{extension}'
            file.save("./static/bukti/" + file_path)
        doc = {
            "totalBelanja":request.form['totalBelanja'],
            "image": file_path  
        }
        db.bukti.insert_one(doc)
        return render_template('riwayat_order.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login'))

@app.route("/riwayat_order", methods=["GET"])
def riwayat_order():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"],
        )
        print(payload)
        riwayat = list(db.transaksi.find({}))
        return render_template('riwayat_order.html', riwayat=riwayat)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('login'))


    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
