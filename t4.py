import tkinter as tk
from tkinter import ttk, messagebox

# ---------- DATA CLASS ----------
class DistribusiMasker:
    def __init__(self, nama_penerima, lokasi, jumlah_masker):
        self.nama_penerima = nama_penerima
        self.lokasi = lokasi
        self.jumlah_masker = jumlah_masker
        self.status_penerimaan = "Belum Terkirim"

    def tandai_terkirim(self):
        self.status_penerimaan = "Terkirim"

class PetugasDistribusi:
    def __init__(self, nama, wilayah_tugas):
        self.nama = nama
        self.wilayah_tugas = wilayah_tugas
        self.daftar_distribusi = []

    def tambah_distribusi(self, distribusi):
        self.daftar_distribusi.append(distribusi)

    def get_distribusi_by_wilayah(self):
        return [d for d in self.daftar_distribusi if d.lokasi == self.wilayah_tugas]

# ---------- GUI CLASS ----------
class AplikasiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Distribusi Masker")
        self.root.geometry("750x500")
        self.root.configure(bg="white")

        self.wilayah_options = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta"]

        # Daftar petugas
        self.petugas_list = {
            "Jakarta": PetugasDistribusi("Andi", "Jakarta"),
            "Bandung": PetugasDistribusi("Budi", "Bandung"),
            "Surabaya": PetugasDistribusi("Citra", "Surabaya"),
            "Yogyakarta": PetugasDistribusi("Dina", "Yogyakarta")
        }

        self.wilayah_var = tk.StringVar(value="Jakarta")
        self.petugas = self.petugas_list["Jakarta"]

        self.buat_sidebar()
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.tampilkan_form()

    def buat_sidebar(self):
        sidebar = tk.Frame(self.root, width=150, bg="#2c3e50")
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(sidebar, text="Form Input", command=self.tampilkan_form,
                  bg="#34495e", fg="white").pack(pady=10, fill="x")
        tk.Button(sidebar, text="Daftar Distribusi", command=self.tampilkan_distribusi,
                  bg="#34495e", fg="white").pack(pady=10, fill="x")

        tk.Label(sidebar, text="Wilayah Tugas:", bg="#2c3e50", fg="white").pack(pady=(30, 5))
        wilayah_menu = ttk.Combobox(sidebar, textvariable=self.wilayah_var,
                                    values=self.wilayah_options, state="readonly")
        wilayah_menu.pack(padx=10, pady=5)
        wilayah_menu.bind("<<ComboboxSelected>>", self.update_wilayah)

    def update_wilayah(self, event=None):
        wilayah = self.wilayah_var.get()
        self.petugas = self.petugas_list[wilayah]
        self.tampilkan_distribusi()

    def tampilkan_form(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Form Input Distribusi Masker", font=("Arial", 16, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=10)

        form_frame = tk.Frame(self.main_frame, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nama Penerima", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(form_frame, text="Lokasi", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(form_frame, text="Jumlah Masker", bg="white").grid(row=2, column=0, sticky="w", pady=5)

        self.ent_nama = tk.Entry(form_frame, bg="#ecf0f1")
        self.ent_lokasi = ttk.Combobox(form_frame, values=self.wilayah_options, state="readonly")
        self.ent_jumlah = tk.Entry(form_frame, bg="#ecf0f1")

        self.ent_nama.grid(row=0, column=1, padx=10, pady=5)
        self.ent_lokasi.grid(row=1, column=1, padx=10, pady=5)
        self.ent_jumlah.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.main_frame, text="Tambah Distribusi", command=self.tambah_data,
                  bg="#1abc9c", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

    def tambah_data(self):
        nama = self.ent_nama.get()
        lokasi = self.ent_lokasi.get()
        jumlah = self.ent_jumlah.get()

        if not nama or not lokasi or not jumlah:
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return

        try:
            jumlah = int(jumlah)
        except ValueError:
            messagebox.showerror("Error", "Jumlah masker harus berupa angka!")
            return

        distribusi = DistribusiMasker(nama, lokasi, jumlah)
        if lokasi in self.petugas_list:
            self.petugas_list[lokasi].tambah_distribusi(distribusi)
        else:
            messagebox.showerror("Error", "Wilayah tidak ditemukan!")

        messagebox.showinfo("Sukses", "Data distribusi ditambahkan!")

        self.ent_nama.delete(0, tk.END)
        self.ent_lokasi.set("")
        self.ent_jumlah.delete(0, tk.END)

    def tampilkan_distribusi(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        wilayah = self.petugas.wilayah_tugas
        nama_petugas = self.petugas.nama

        tk.Label(self.main_frame, text=f"Daftar Distribusi Wilayah: {wilayah}", font=("Arial", 14, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=(10, 5))

        tk.Label(self.main_frame, text=f"Petugas: {nama_petugas}", font=("Arial", 12),
                 bg="white", fg="#34495e").pack(pady=(0, 10))

        self.tree = ttk.Treeview(self.main_frame, columns=("Nama", "Lokasi", "Jumlah", "Status"), show="headings")
        for col in ("Nama", "Lokasi", "Jumlah", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(pady=10, fill="x")

        for dist in self.petugas.get_distribusi_by_wilayah():
            self.tree.insert("", "end", values=(
                dist.nama_penerima,
                dist.lokasi,
                dist.jumlah_masker,
                dist.status_penerimaan
            ))

        tk.Button(self.main_frame, text="Tandai Terkirim", command=self.tandai_terkirim,
                  bg="#e67e22", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def tandai_terkirim(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih salah satu data distribusi!")
            return

        values = self.tree.item(selected_item, "values")
        for dist in self.petugas.daftar_distribusi:
            if (dist.nama_penerima, dist.lokasi, dist.jumlah_masker) == (values[0], values[1], int(values[2])):
                dist.tandai_terkirim()
                break

        self.tampilkan_distribusi()

# ---------- JALANKAN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiGUI(root)
    root.mainloop()