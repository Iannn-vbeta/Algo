import csv
import datetime
import os

file_path = './gudang.csv'

def baca_data():
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ['nama', 'jumlah', 'tanggal_masuk', 'kategori']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        return []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def tulis_data(data):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['nama', 'jumlah', 'tanggal_masuk', 'kategori']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def selection_sort_tanggal(data):
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data[j]['tanggal_masuk'] < data[min_idx]['tanggal_masuk']:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


def linear_search_nama(data, nama_barang):
    hasil_pencarian = []
    for row in data:
        if row['nama'][:3].lower() == nama_barang.lower():
            hasil_pencarian.append(row)
    return hasil_pencarian


def linear_search_tanggal(data, tanggal_masuk):
    hasil_pencarian = []
    for row in data:
        if row['tanggal_masuk'] == tanggal_masuk:
            hasil_pencarian.append(row)
    return hasil_pencarian


def pencarian_barang(data_gudang):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==========================================")
        print("            Pencarian Barang")
        print("==========================================")
        print("1. Cari berdasarkan Nama Barang")
        print("2. Cari berdasarkan Tanggal Masuk")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih opsi (1-2) atau 0 untuk kembali: ")

        if pilihan == '1':
            nama_barang = input("Masukkan 3 huruf pertama dari nama barang: ")
            hasil = linear_search_nama(data_gudang, nama_barang)
            if hasil:
                print("Hasil Pencarian Berdasarkan Nama Barang:")
                for row in hasil:
                    print(row)
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali ke menu.")
        elif pilihan == '2':
            tanggal_masuk = input("Masukkan tanggal masuk (YYYY-MM-DD): ")
            hasil = linear_search_tanggal(data_gudang, tanggal_masuk)
            if hasil:
                print("Hasil Pencarian Berdasarkan Tanggal Masuk:")
                for row in hasil:
                    print(row)
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali ke menu.")
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
            input("\nTekan Enter untuk kembali ke menu.")

# Fungsi utama untuk menjalankan program
def main():
    data_gudang = baca_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==========================================")
        print("         Sistem Manajemen Gudang")
        print("==========================================")
        print("1. Pengurutan Otomatis Berdasarkan Tanggal Masuk")
        print("2. Pencarian Barang")
        print("3. Pemberitahuan Stok Hampir Habis")
        print("4. Pengelompokan Barang Berdasarkan Kategori")
        print("5. Manajemen Persediaan")
        print("==========================================")
        pilihan = input("Pilih opsi (1-5) atau 0 untuk keluar: ")

        if pilihan == '1':
            # Implementasi fitur 1: Pengurutan Otomatis
            data_terurut = selection_sort_tanggal(data_gudang)
            for row in data_terurut:
                print(row)
            input("\nTekan Enter untuk kembali ke menu.")
        
        elif pilihan == '2':
            # Implementasi fitur 2: Pencarian Barang
            pencarian_barang(data_gudang)
        
        elif pilihan == '3':
            # Implementasi fitur 3: Pemberitahuan Stok Hampir Habis
            ambang_batas = int(input("Masukkan ambang batas stok: "))
            stok_hampir_habis = []
            for row in data_gudang:
                if int(row['jumlah']) <= ambang_batas:
                    stok_hampir_habis.append(row)
            if stok_hampir_habis:
                print("Barang dengan stok hampir habis:")
                for row in stok_hampir_habis:
                    print(row)
            else:
                print("Tidak ada barang dengan stok hampir habis.")
            input("\nTekan Enter untuk kembali ke menu.")
        
        elif pilihan == '4':
            # Implementasi fitur 4: Pengelompokan Barang Berdasarkan Kategori
            def divide_and_conquer(data_list):
                if len(data_list) <= 1:
                    return data_list
                mid = len(data_list) // 2
                left = divide_and_conquer(data_list[:mid])
                right = divide_and_conquer(data_list[mid:])
                return merge(left, right)
            
            def merge(left, right):
                result = []
                while left and right:
                    if left[0]['kategori'] <= right[0]['kategori']:
                        result.append(left.pop(0))
                    else:
                        result.append(right.pop(0))
                result.extend(left if left else right)
                return result
            
            sorted_data_list = divide_and_conquer(data_gudang)
            if sorted_data_list:
                print("Pengelompokan Barang Berdasarkan Kategori:")
                for row in sorted_data_list:
                    print(row)
            else:
                print("Tidak ada data barang untuk dikelompokkan.")
            input("\nTekan Enter untuk kembali ke menu.")
        
        elif pilihan == '5':
            # Implementasi fitur 5: Manajemen Persediaan
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("==========================================")
                print("        Manajemen Persediaan Barang")
                print("==========================================")
                print("1. Tambah Barang")
                print("2. Hapus Barang")
                print("3. Update Jumlah Barang")
                print("0. Kembali ke Menu Utama")
                sub_pilihan = input("Pilih opsi (1-3) atau 0 untuk kembali: ")

                if sub_pilihan == '1':
                    # Tambah Barang
                    nama = input("Masukkan nama barang: ")
                    jumlah = input("Masukkan jumlah barang: ")
                    data_gudang.append({'nama': nama, 'jumlah': jumlah, 'tanggal_masuk': datetime.datetime.now().strftime("%Y-%m-%d")})
                    while True:
                        print("==========================================")
                        print("        Manajemen Persediaan Barang")
                        print("==========================================")
                        print("1. Alat")
                        print("2. Pupuk")
                        print("3. Benih")
                        print("4. Pakan")
                        print("5. Hasil Panen")
                        print("0. Kembali ke Menu Utama")
                        sub_sub_pilihan = input("Pilih opsi (1-5) atau 0 untuk kembali: ")
                            
                        if sub_sub_pilihan == '1':
                            data_gudang.append({'kategori':'Alat'})
                        elif sub_sub_pilihan == '2':
                            data_gudang.append({'kategori':'Pupuk'})
                        elif sub_sub_pilihan == '3':
                            data_gudang.append({'kategori':'Benih'})
                        elif sub_sub_pilihan == '4':
                            data_gudang.append({'kategori':'Pakan'})
                        elif sub_sub_pilihan == '5':
                            data_gudang.append({'kategori':'Hasil Panen'})
                        elif sub_pilihan == 0:
                            break
                        else:
                            print("Pilihan tidak valid, coba lagi.")
                            input("\nTekan Enter untuk kembali ke menu.")
                    print("Barang berhasil ditambahkan.")
                    tulis_data(data_gudang)
                    input("\nTekan Enter untuk kembali ke menu.")
                
                elif sub_pilihan == '2':
                    # Hapus Barang
                    nama = input("Masukkan nama barang yang ingin dihapus: ")
                    data_gudang = [row for row in data_gudang if row['nama'] != nama]
                    print("Barang berhasil dihapus.")
                    tulis_data(data_gudang)
                    input("\nTekan Enter untuk kembali ke menu.")
                
                elif sub_pilihan == '3':
                    # Update Jumlah Barang
                    nama = input("Masukkan nama barang yang ingin diupdate: ")
                    jumlah = input("Masukkan jumlah baru barang: ")
                    found = False
                    for row in data_gudang:
                        if row['nama'] == nama:
                            row['jumlah'] = jumlah
                            found = True
                            break
                    if not found:
                        print("Data tidak sesuai")
                    else:
                        print("Jumlah barang berhasil diupdate.")
                    tulis_data(data_gudang)
                    input("\nTekan Enter untuk kembali ke menu.")
                
                elif sub_pilihan == '0':
                    break
                
                else:
                    print("Pilihan tidak valid, coba lagi.")
                    input("\nTekan Enter untuk kembali ke menu.")

        elif pilihan == '0':
            print("Keluar dari sistem.")
            break
        
        else:
            print("Pilihan tidak valid, coba lagi.")
            input("\nTekan Enter untuk kembali ke menu.")

# Menjalankan program
if __name__ == "__main__":
    main()

