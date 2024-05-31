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
    nama_barang = nama_barang.lower()  
    for row in data:
        if nama_barang in row['nama'].lower():  
            hasil_pencarian.append(row)
    return hasil_pencarian

def linear_search_tanggal(data, tanggal_masuk):
    hasil_pencarian = []
    tanggal_masuk = tanggal_masuk.lower()  
    for row in data:
        if tanggal_masuk in row['tanggal_masuk'].lower(): 
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
            #fitur 1: Pengurutan Otomatis
            data_terurut = selection_sort_tanggal(data_gudang)
            for row in data_terurut:
                print(row)
            input("\nTekan Enter untuk kembali ke menu.")
        
        elif pilihan == '2':
            #fitur 2: Pencarian Barang
            pencarian_barang(data_gudang)
        
        elif pilihan == '3':
            #fitur 3: Pemberitahuan Stok Hampir Habis
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
            #fitur 4: Pengelompokan Barang Berdasarkan Kategori
            def moco(filename):
                with open(filename, mode='r') as file:
                    csv_reader = csv.DictReader(file)
                    items = [row for row in csv_reader]
                return items 

            def divide(items):
                if len(items) <= 1:
                    return items
                mid = len(items) // 2
                left = divide(items[:mid])
                right = divide(items[mid:])
                return [left, right]


            def conquer(items):
                if isinstance(items[0], dict):  
                    grouped = {}
                    for item in items:
                        category = item['kategori']
                        if category not in grouped:
                            grouped[category] = []
                        grouped[category].append(item)
                    return grouped
                else:  
                    left_grouped = conquer(items[0])
                    right_grouped = conquer(items[1])
                    return combine(left_grouped, right_grouped)


            def combine(left, right):
                combined = {}
                for key, value in left.items():
                    combined[key] = combined.get(key, []) + value
                for key, value in right.items():
                    combined[key] = combined.get(key, []) + value
                return combined

            def categorize_items(filename):
                items = moco(filename)
                divided_items = divide(items)
                grouped_items = conquer(divided_items)
                return grouped_items

            def tampilkan_tabel(grouped_items, selected_category=None):
                if selected_category:
                    categories = [selected_category]
                else:
                    categories = grouped_items.keys()

                print("|" + "=" * 65 + "|")
                print("|" + " " * 25 + "Pencarian Barang" + " " * 24 + "|")
                print("|" + "=" * 65 + "|")

                for category in categories:
                    if category in grouped_items:
                        items = grouped_items[category]
                        print("|" + "=" * 65 + "|")
                        print(f"| Kategori: {category} "+ " "*(53-(len(category)))+"|")
                        print("|" + "-" * 65 + "|")
                        print("| Nama" + " " * 26 + "| Jumlah" + " " * 9 + "| Tanggal Masuk  |")
                        print("|" + "-" * 65 + "|")
                        for item in items:
                            nama = item['nama']
                            jumlah = item['jumlah']
                            tanggal_masuk = item['tanggal_masuk']
                            print(f"| {nama}" + " " * (30 - len(nama)) + f"| {jumlah}" + " " * (15 - len(jumlah)) + f"| {tanggal_masuk}" + " " * (15 - len(tanggal_masuk)) + "|")
                        print("|" + "-" * 65 + "|")
                        print()
                        input("\nTekan Enter untuk kembali ke menu.")

            filename = 'gudang.csv'

            grouped_items = categorize_items(filename)

            print("Pilih kategori untuk ditampilkan:")
            print("1. Semua")
            print("2. Bibit")
            print("3. Peralatan")
            print("4. Obat")
            print("5. Mesin")
            print("6. Tanaman")
            choice = input("Masukkan pilihan Anda (1-6): ")

            category_mapping = {
                "1": None,
                "2": "Bibit",
                "3": "Peralatan",
                "4": "Obat",
                "5": "Mesin",
                "6": "Tanaman"
            }

            selected_category = category_mapping.get(choice, None)

            tampilkan_tabel(grouped_items, selected_category)
            break
        
        elif pilihan == '5':
            #fitur 5: Manajemen Persediaan
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("==========================================")
                print("        Manajemen Persediaan Barang       ")
                print("==========================================")
                print("1. Tambah Barang")
                print("2. Hapus Barang")
                print("3. Update Jumlah Barang")
                print("0. Kembali ke Menu Utama")
                sub_pilihan = input("Pilih opsi (1-3) atau 0 untuk kembali: ")

                if sub_pilihan == '1':
                    # Tambah Barang
                    nama = input("Masukkan nama barang: ")
                    if any(row['nama'].lower() == nama.lower() for row in data_gudang):
                        print("Barang dengan nama tersebut sudah ada.")
                        input("\nTekan Enter untuk kembali ke menu.")
                        continue
                    jumlah = input("Masukkan jumlah barang: ")
                    tanggal_masuk = input("Masukkan tanggal masuk (YYYY-MM-DD) atau kosongkan untuk tanggal hari ini: ")
                    if not tanggal_masuk:
                        tanggal_masuk = datetime.datetime.now().strftime("%Y-%m-%d")
                    kategori = ""
                    while True:
                        print("==========================================")
                        print("        Kategori Barang")
                        print("==========================================")
                        print("1. Peralatan")
                        print("2. Pupuk")
                        print("3. Benih")
                        print("4. Obat")
                        print("5. Mesin")
                        print("0. Kembali ke Menu Utama")
                        sub_sub_pilihan = input("Pilih kategori (1-5) atau 0 untuk kembali: ")
                            
                        if sub_sub_pilihan == '1':
                            kategori = 'Peralatan'
                            break
                        elif sub_sub_pilihan == '2':
                            kategori = 'Pupuk'
                            break
                        elif sub_sub_pilihan == '3':
                            kategori = 'Benih'
                            break
                        elif sub_sub_pilihan == '4':
                            kategori = 'Obat'
                            break
                        elif sub_sub_pilihan == '5':
                            kategori = 'Mesin'
                            break
                        elif sub_sub_pilihan == '0':
                            break
                        else:
                            print("Pilihan tidak valid, coba lagi.")
                            input("\nTekan Enter untuk kembali ke menu.")
                    
                    if kategori:
                        data_gudang.append({'nama': nama, 'jumlah': jumlah, 'tanggal_masuk': tanggal_masuk, 'kategori': kategori})
                        print("Barang berhasil ditambahkan.")
                        tulis_data(data_gudang)
                    else:
                        print("Barang tidak ditambahkan, kategori tidak dipilih.")
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

