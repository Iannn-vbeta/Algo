import pandas as pd

# Membaca data dari file CSV
def baca_data_gudang(file_path):
    return pd.read_csv(file_path)

def selection_sort_tanggal(data):
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data.iloc[j]['tanggal_masuk'] < data.iloc[min_idx]['tanggal_masuk']:
                min_idx = j
        if min_idx != i:
            # Tukar posisi data
            data.iloc[i], data.iloc[min_idx] = data.iloc[min_idx].copy(), data.iloc[i].copy()
    return data

def linear_search_nama(data, nama_barang):
    hasil_pencarian = []
    for index, row in data.iterrows():
        if nama_barang.lower() in row['nama'].lower():
            hasil_pencarian.append(row)
    return pd.DataFrame(hasil_pencarian)

def linear_search_tanggal(data, tanggal_masuk):
    hasil_pencarian = []
    for index, row in data.iterrows():
        if row['tanggal_masuk'] == tanggal_masuk:
            hasil_pencarian.append(row)
    return pd.DataFrame(hasil_pencarian)

def pemberitahuan_stok_hampir_habis(data, ambang_batas):
    stok_hampir_habis = []
    for index, row in data.iterrows():
        if row['jumlah'] <= ambang_batas:
            stok_hampir_habis.append(row)
    return pd.DataFrame(stok_hampir_habis)

def pengelompokan_kategori(data):
    kelompok = {}
    for index, row in data.iterrows():
        kategori = row['kategori']
        if kategori in kelompok:
            kelompok[kategori].append(row)
        else:
            kelompok[kategori] = [row]
    return kelompok

def manajemen_persediaan(data, nama_barang, jumlah, operasi):
    for index, row in data.iterrows():
        if row['nama'] == nama_barang:
            if operasi == 'tambah':
                data.at[index, 'jumlah'] += jumlah
            elif operasi == 'kurang':
                data.at[index, 'jumlah'] -= jumlah
    return data

def menu(data_gudang):
    while True:
        print("==========================================")
        print("         Sistem Manajemen Gudang")
        print("==========================================")
        print("1. Pengurutan Otomatis Berdasarkan Tanggal Masuk")
        print("2. Pencarian Barang")
        print("3. Pemberitahuan Stok Hampir Habis")
        print("4. Pengelompokan Barang Berdasarkan Kategori")
        print("5. Manajemen Persediaan")
        print("0. Keluar dari Sistem")
        print("==========================================")
        pilihan = input("Pilih opsi (1-5) atau 0 untuk keluar: ")
        
        if pilihan == '1':
            data_terurut = selection_sort_tanggal(data_gudang.copy())
            print("Data Terurut Berdasarkan Tanggal Masuk:")
            print(data_terurut)
        elif pilihan == '2':
            sub_pilihan = input("Cari berdasarkan (1) Nama atau (2) Tanggal Masuk: ")
            if sub_pilihan == '1':
                nama_barang = input("Masukkan nama barang: ")
                hasil = linear_search_nama(data_gudang, nama_barang)
                print("Hasil Pencarian Berdasarkan Nama:")
                print(hasil)
            elif sub_pilihan == '2':
                tanggal_masuk = input("Masukkan tanggal masuk (YYYY-MM-DD): ")
                hasil = linear_search_tanggal(data_gudang, tanggal_masuk)
                print("Hasil Pencarian Berdasarkan Tanggal Masuk:")
                print(hasil)
        elif pilihan == '3':
            ambang_batas = int(input("Masukkan ambang batas stok: "))
            stok_hampir_habis = pemberitahuan_stok_hampir_habis(data_gudang, ambang_batas)
            print("Barang dengan Stok Hampir Habis:")
            print(stok_hampir_habis)
        elif pilihan == '4':
            data_kelompok = pengelompokan_kategori(data_gudang)
            print("Data Kelompok Barang Berdasarkan Kategori:")
            for kategori, items in data_kelompok.items():
                print(f"Kategori: {kategori}")
                for item in items:
                    print(item)
                print()
        elif pilihan == '5':
            nama_barang = input("Masukkan nama barang: ")
            jumlah = int(input("Masukkan jumlah: "))
            operasi = input("Operasi (tambah/kurang): ")
            data_gudang = manajemen_persediaan(data_gudang.copy(), nama_barang, jumlah, operasi)
            print("Data persediaan diperbarui.")
            print(data_gudang)
        elif pilihan == '0':
            print("Keluar dari sistem.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

# Fungsi utama untuk menjalankan program
def main():
    file_path = 'gudang.csv'
    data_gudang = baca_data_gudang(file_path)
    menu(data_gudang)

if __name__ == "__main__":
    main()
