import csv
import datetime
import os
from ptabel import PTable

file_path = './gudang.csv'

def baca_data(filename=file_path):
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

def catat_barang_keluar(file_path,nama_barang,jumlah_barang,tanggal_keluar=None):
    tanggal_keluar = tanggal_keluar or datetime.datetime.now().strftime("%Y-%m-%d")
    list_barang = baca_data(file_path)
    for row in list_barang:
        if row['nama'] == nama_barang:
            row['jumlah'] = str(int(row['jumlah']) - jumlah_barang)
            break
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['nama', 'jumlah', 'tanggal_masuk', 'kategori']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list_barang)
    with open('./barang_keluar.csv', mode='a', newline='') as file:
        fieldnames = ['nama', 'jumlah', 'tanggal_keluar']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'nama': nama_barang, 'jumlah': jumlah_barang, 'tanggal_keluar': tanggal_keluar})

def totals(data):
    total = 0
    for item in data:
        total += item
    return total

def sortdict(data, key=None, reverse=False):
    sorted_data = data[:]
    for i in range(len(sorted_data) - 1):
        min_idx = i
        for j in range(i + 1, len(sorted_data)):
            if key is not None:
                if key(sorted_data[j]) < key(sorted_data[min_idx]):
                    min_idx = j
            else:
                if sorted_data[j] < sorted_data[min_idx]:
                    min_idx = j
        sorted_data[i], sorted_data[min_idx] = sorted_data[min_idx], sorted_data[i]
    if reverse:
        sorted_data.reverse()
    return sorted_data

def statistik_barang_keluar():
    data_barang_keluar = []
    
    with open('./barang_keluar.csv', mode='r') as file:
        reader = csv.DictReader(file)
        data_barang_keluar = [row for row in reader]
    data_aggregated = {}
    
    for row in data_barang_keluar:
        nama = row['nama']
        jumlah = int(row['jumlah'])
        if nama in data_aggregated:
            data_aggregated[nama] += jumlah
        else:
            data_aggregated[nama] = jumlah
            
    aggregated_data = [{'nama': nama, 'jumlah': jumlah} for nama, jumlah in data_aggregated.items()]
    
    total_jumlah = totals([row['jumlah'] for row in aggregated_data])

    sorted_data = sortdict(aggregated_data, key=lambda x: x['jumlah'], reverse=True)

    x = PTable(["Nama", "Jumlah", "Persentase"])
    for row in sorted_data:
        persentase = row['jumlah'] / total_jumlah * 100
        x.add_row([row['nama'], row['jumlah'], f"{persentase:.2f}%"])

    x.print()
    print(f"Total Jumlah Barang Keluar: {total_jumlah}")
    return total_jumlah

def statistik_gudang(data_gudang):
    total_barang = len(data_gudang)
    total_jumlah = totals([int(row['jumlah']) for row in data_gudang])
    total_barang_per_kategori = {}
    for row in data_gudang:
        kategori = row['kategori']
        if kategori not in total_barang_per_kategori:
            total_barang_per_kategori[kategori] = 0
        total_barang_per_kategori[kategori] += int(row['jumlah'])
    dict_return = {
        'total_barang': total_barang,
        'total_jumlah': total_jumlah,
        'total_barang_per_kategori': total_barang_per_kategori
    }
    x = PTable(["Kategori", "Total Barang", "Persentase", "Jumlah Barang", "Persentase"])
    for kategori, total in total_barang_per_kategori.items():
        persentase = total / total_jumlah * 100
        jumlah_entitas = len([row for row in data_gudang if row['kategori'] == kategori])
        persentase_entitas = jumlah_entitas / total_barang * 100
        x.add_row([kategori, total, f"{persentase:.2f}%", jumlah_entitas, f"{persentase_entitas:.2f}%"])
    x.add_title("Barang per Kategori")
    x.print()
    print(f"Total Barang: {total_barang}")
    print(f"Total Jumlah Barang: {total_jumlah}")
    return dict_return

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


def pemberitahuan_stok_habis(data_gudang, ambang_batas):
    stok_hampir_habis = []
    for row in data_gudang:
        if int(row['jumlah']) <= ambang_batas:
            stok_hampir_habis.append(row)
    return stok_hampir_habis

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
                x = PTable(["Nama", "Jumlah", "Tanggal Masuk", "Kategori"])
                for row in hasil:
                    x.add_row([row['nama'], row['jumlah'], row['tanggal_masuk'], row['kategori']])
                x.print()
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali ke menu.")
        elif pilihan == '2':
            tanggal_masuk = input("Masukkan tanggal masuk (YYYY-MM-DD): ")
            hasil = linear_search_tanggal(data_gudang, tanggal_masuk)
            if hasil:
                x = PTable(["Nama", "Jumlah", "Tanggal Masuk", "Kategori"])
                for row in hasil:
                    x.add_row([row['nama'], row['jumlah'], row['tanggal_masuk'], row['kategori']])
                x.print()
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
            x = PTable(["Nama", "Jumlah", "Tanggal Masuk", "Kategori"])
            for row in data_terurut:
                x.add_row([row['nama'], row['jumlah'], row['tanggal_masuk'], row['kategori']])
            x.print()
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
                items = baca_data(filename)
                divided_items = divide(items)
                grouped_items = conquer(divided_items)
                return grouped_items

            def tampilkan_tabel(grouped_items, selected_category=None):
                if selected_category:
                    categories = [selected_category]
                else:
                    categories = grouped_items.keys()
                for category in categories:
                    if category in grouped_items:
                        items = grouped_items[category]
                        x = PTable(["Nama", "Jumlah", "Tanggal Masuk"])
                        x.add_title(f"Kategori: {category}")
                        for item in items:
                            x.add_row([item['nama'], item['jumlah'], item['tanggal_masuk']])
                        x.print()    
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
            print("0. Kembali ke Menu Utama")
            while True:
                print("                                                                                         ",end="",flush=True)
                print("\rMasukkan pilihan Anda (1-5): ",end="",flush=True)
                choice = input()
                print(f"\033[F", end="", flush=True)
                if choice == '0':
                    break
                elif choice not in ['1', '2', '3', '4', '5']:
                    print(f"\033[K\rPilihan tidak valid, Tekan Enter untuk kembali memilih.",end="",flush=True)
                    input()
                    print(f"\033[F", end="", flush=True)
                    continue 
                category_mapping = {
                    "1": None,
                    "2": "Bibit",
                    "3": "Peralatan",
                    "4": "Obat",
                    "5": "Mesin"
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
                print("4. Barang Keluar")
                print("5. Statistik Barang Keluar")
                print("6. Statistik Gudang")
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
                    data_hapus = [row for row in data_gudang if row['nama'] == nama]
                    if len(data_hapus) != 0:
                        data_gudang = [row for row in data_gudang if row['nama'] != nama]
                        print("Barang berhasil dihapus.")
                        tulis_data(data_gudang)
                    else:
                        print("Data tidak sesuai")
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
                    
                elif sub_pilihan =="4":
                    x = PTable(["Nama", "Jumlah", "Tanggal Masuk", "Kategori"])
                    for row in data_gudang:
                        x.add_row([row['nama'], row['jumlah'], row['tanggal_masuk'], row['kategori']])
                    x.print()
                    
                    nama = input("Masukkan nama barang yang keluar: ")
                    jumlah = input("Masukkan jumlah barang yang keluar: ")
                    for row in data_gudang:
                        if row['nama'] == nama:
                            if int(row['jumlah']) < int(jumlah):
                                print("Jumlah barang tidak mencukupi.")
                                break
                            row['jumlah'] = str(int(row['jumlah']) - int(jumlah))
                            print("Barang berhasil keluar.")
                            tulis_data(data_gudang)
                            break
                    tanggal_keluar = input("Masukkan tanggal keluar (YYYY-MM-DD) atau kosongkan untuk tanggal hari ini: ")
                    if not tanggal_keluar:
                        tanggal_keluar = datetime.datetime.now().strftime("%Y-%m-%d")
                    catat_barang_keluar(file_path,nama,int(jumlah),tanggal_keluar)
                    input("\nTekan Enter untuk kembali ke menu.")
                elif sub_pilihan == '5':
                    statistik_barang_keluar()
                    input("\nTekan Enter untuk kembali ke menu.")
                elif sub_pilihan == '6':
                    statistik_gudang(data_gudang)
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

