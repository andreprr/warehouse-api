
# 📦 Stock Warehouse API Take Home Assignment Task 2 - Katekima Dibuat dengan Django + Django REST Framework Warehouse system untuk mengelola: 
- 📦 Items
-  🛒 Purchases (stok masuk)
-  💸 Sells (stok keluar)
-  📊 Laporan pergerakan stok (FIFO) dalam JSON

# 🚀 Cara Menjalankan Project 
## 1. Clone project dan masuk folder assignment 
```
 git clone https://github.com/andreprr/warehouse-api.git cd warehouse-api/test2/
```
## 2. Buat virtual environment & install dependencies 
```
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

 ## 3. Migrasi database dan jalankan server 
```
python manage.py migrate
python manage.py runserver
```

--- # 🔗 API ENDPOINTS 
 ## ✅ Items 
```
GET /items/ # List semua item
POST /items/ # Tambah item
GET /items/{code}/ # Lihat detail item
PUT /items/{code}/ # Edit item
DELETE /items/{code}/ # Soft delete item
```

 ## ✅ Purchase 
```
POST /purchase/ # Buat header pembelian
POST /purchase/{code}/details/ # Tambah detail pembelian (update stock & balance)
GET /purchase/ # Lihat semua pembelian
```

 ## ✅ Sell 
```
POST /sell/ # Buat header penjualan
POST /sell/{code}/details/ # Tambah detail penjualan (kurangi stock & balance)
GET /sell/ # Lihat semua penjualan
```

 ## ✅ Report 
```
GET /report/{item_code}/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD # Hasil laporan berupa JSON dengan rincian transaksi dan FIFO balance
```

--- # 📌 Catatan 
- Semua model menggunakan soft delete (is_deleted = True)
- Transaksi otomatis update stock dan balance
- Laporan report JSON mengikuti FIFO logic
--- #

 📎 Teknologi 
```
 Python >= 3.12 Django >= 5.1.3 Django REST Framework >= 3.15.2
```
