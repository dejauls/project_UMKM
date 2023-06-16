from flask import Flask, render_template, request
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = "mongodb://jaul:kelompok4@ac-tckcnrv-shard-00-00.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-01.iyckasz.mongodb.net:27017,ac-tckcnrv-shard-00-02.iyckasz.mongodb.net:27017/?ssl=true&replicaSet=atlas-ehh9a0-shard-0&authSource=admin&retryWrites=true&w=majority"
DB_NAME =  "umkm"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/daftar_user')
def user():
    collection = db.users
    users = collection.find({})
   
    return render_template('daftar_user.html',
                            users=users
                            )

@app.route('/list_order')
def orderan():
    return render_template('transaksi_admin.html')

@app.route('/katalog-admin')
def admincat():
    return render_template('admin_cat.html')

@app.route('/inputkatalog')
def inputkatalog():
    return render_template('inputkatalog.html')


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


#untuk page transaksi admin
        #def get_orders():
            #client = MongoClient('mongodb://localhost:27017/')  # Ganti URL MongoDB sesuai konfigurasi Anda
            #db = client['order_database']  # Ganti nama database sesuai dengan nama database Anda
            #collection = db['orders']  # Ganti nama koleksi sesuai dengan nama koleksi Anda
            #orders = collection.find()
            #return orders

        #@app.route('/')
        #def home():
            #orders = get_orders()
            #return render_template('index.html', orders=orders)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)