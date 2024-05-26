import pandas as pd

def baca_data_gudang(file_path):
    return pd.read_csv(file_path)

def selection_sort_tanggal(data):
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data.at[j, 'tanggal_masuk'] < data.at[min_idx, 'tanggal_masuk']:
                min_idx = j
        if min_idx != i:
            temp = data.loc[i].copy()
            data.loc[i] = data.loc[min_idx]
            data.loc[min_idx] = temp
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
    def divide_conquer(data):
        if len(data) <= 1:
            return {data.iloc[0]['kategori']: [data.iloc[0]]}

        mid = len(data) // 2
        left = divide_conquer(data.iloc[:mid])
        right = divide_conquer(data.iloc[mid:])

        merged = {}
        for key in left:
            if key in right:
                merged[key] = left[key] + right[key]
            else:
                merged[key] = left[key]
        for key in right:
            if key not in merged:
                merged[key] = right[key]

        return merged

    data_dict = divide_conquer(data)
    return data_dict

def manajemen_persediaan(data, nama_barang, jumlah, operasi, file_path):
    if operasi == 'tambah':
        if data[data['nama'] == nama_barang].empty:
            data_baru = pd.DataFrame({'nama': [nama_barang], 'jumlah': [jumlah]})
            data = pd.concat([data, data_baru], ignore_index=True)
        else:
            data.loc[data['nama'] == nama_barang, 'jumlah'] += jumlah
    elif operasi == 'kurang':
        data.loc[data['nama'] == nama_barang, 'jumlah'] -= jumlah
        data = data[data['jumlah'] > 0]

    data.to_csv(file_path, index=False)
    return data

def menu(file_path):
    data_gudang = baca_data_gudang(file_path)
    
    while True:
        print("==========================================")
        print("         Sistem Manajemen Gudang")
        print("==========================================")
        print("1. Pengurutan Otomatis Berdasarkan Tanggal Masuk")
        print("2. Pencarian Barang")
        print("3. Pemberitahuan Stok Hampir Habis")
        print("4. Pengelompokan Barang Berdasarkan Kategori (Divide and Conquer)")
        print("5. Manajemen Persediaan (Create, Read, Update, Delete)")
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
            while True:
                print("==========================================")
                print("   Manajemen Persediaan (Create, Read, Update, Delete)")
                print("==========================================")
                print("1. Tambah Barang")
                print("2. Lihat Data Persediaan")
                print("3. Update Jumlah Barang")
                print("4. Hapus Barang")
                print("0. Kembali ke Menu Utama")
                sub_pilihan = input("Pilih opsi (1-4) atau 0 untuk kembali: ")
                
                if sub_pilihan == '1':
                    nama_barang = input("Masukkan nama barang baru: ")
                    jumlah = int(input("Masukkan jumlah barang: "))
                    manajemen_persediaan(data_gudang.copy(), nama_barang, jumlah, 'tambah', file_path)
                    print("Barang baru berhasil ditambahkan.")
                elif sub_pilihan == '2':
                    print("Data Persediaan Saat Ini:")
                    print(data_gudang)
                elif sub_pilihan == '3':
                    nama_barang = input("Masukkan nama barang: ")
                    jumlah = int(input("Masukkan jumlah baru: "))
                    manajemen_persediaan(data_gudang.copy(), nama_barang, jumlah, 'kurang', file_path)
                    print("Jumlah barang berhasil diupdate.")
                elif sub_pilihan == '4':
                    nama_barang = input("Masukkan nama barang yang ingin dihapus: ")
                    manajemen_persediaan(data_gudang.copy(), nama_barang, 0, 'kurang', file_path)
                    print("Barang berhasil dihapus.")
                elif sub_pilihan == '0':
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
        elif pilihan == '0':
            print("Keluar dari sistem.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

def main():
    file_path = 'gudang.csv'
    menu(file_path)

if __name__ == "__main__":
    main()
