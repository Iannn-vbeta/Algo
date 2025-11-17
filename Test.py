import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def generate_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

def add_task():
    tasks = load_tasks()
    title = input("Judul tugas     : ")
    desc = input("Deskripsi tugas : ")
    deadline = input("Deadline (YYYY-MM-DD) : ")

    new_task = {
        "id": generate_id(tasks),
        "title": title,
        "description": desc,
        "deadline": deadline,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print("\n✓ Tugas berhasil ditambahkan!\n")

def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\nTidak ada tugas.\n")
        return

    print("\n===== DAFTAR TUGAS =====")
    for t in tasks:
        print(f"""
ID         : {t['id']}
Judul      : {t['title']}
Deskripsi  : {t['description']}
Deadline   : {t['deadline']}
Status     : {t['status']}
Dibuat     : {t['created_at']}
-----------------------------""")

def update_status():
    tasks = load_tasks()
    show_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang akan diupdate: "))
    except ValueError:
        print("Input tidak valid!")
        return
    
    for t in tasks:
        if t["id"] == task_id:
            print("\n1. Pending\n2. In Progress\n3. Selesai")
            choice = input("Pilih status: ")

            mapping = {"1": "Pending", "2": "In Progress", "3": "Selesai"}
            t["status"] = mapping.get(choice, t["status"])
            save_tasks(tasks)
            print("✓ Status tugas diperbarui!\n")
            return
    
    print("ID tidak ditemukan!")

def delete_task():
    tasks = load_tasks()
    show_tasks()
    try:
        task_id = int(input("\nMasukkan ID tugas yang akan dihapus: "))
    except ValueError:
        print("Input tidak valid!")
        return
    
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print("✓ Tugas berhasil dihapus!\n")


def main():
    while True:
        print("""
===== TASK MANAGEMENT =====
1. Tambah Tugas
2. Lihat Semua Tugas
3. Update Status Tugas
4. Hapus Tugas
5. Keluar
""")
        choice = input("Pilih menu: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            update_status()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
