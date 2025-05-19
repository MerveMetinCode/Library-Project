import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_database = os.getenv("MYSQL_DATABASE")

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Veritabanı Hatası", f"Bağlantı hatası: {err}")
        return None


def kitap_ekle(conn, ad, yazar, yayinevi, yayin_yili, kategori):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO kitaplar (ad, yazar, yayinevi, yayin_yili, kategori) VALUES (%s, %s, %s, %s, %s)"
            values = (ad, yazar, yayinevi, yayin_yili, kategori)
            cursor.execute(sql, values)
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Kitap eklenemedi: {err}")

def kitaplari_listele(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM kitaplar")
            return cursor.fetchall()
    except mysql.connector.Error as err:
        messagebox.showerror("Hata", f"Kitaplar alınamadı: {err}")
        return []

def kitap_ekle_gui():
    def ekle():
        conn = get_connection()
        if conn:
            try:
                kitap_ekle(conn, entry_ad.get(), entry_yazar.get(), entry_yayinevi.get(), int(entry_yil.get()), entry_kategori.get())
                messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi!")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
            finally:
                conn.close()

    pencere = tk.Toplevel(root)
    pencere.title("Kitap Ekle")

    tk.Label(pencere, text="Kitap Adı").grid(row=0, column=0)
    entry_ad = tk.Entry(pencere)
    entry_ad.grid(row=0, column=1)

    tk.Label(pencere, text="Yazar").grid(row=1, column=0)
    entry_yazar = tk.Entry(pencere)
    entry_yazar.grid(row=1, column=1)

    tk.Label(pencere, text="Yayınevi").grid(row=2, column=0)
    entry_yayinevi = tk.Entry(pencere)
    entry_yayinevi.grid(row=2, column=1)

    tk.Label(pencere, text="Yayın Yılı").grid(row=3, column=0)
    entry_yil = tk.Entry(pencere)
    entry_yil.grid(row=3, column=1)

    tk.Label(pencere, text="Kategori").grid(row=4, column=0)
    entry_kategori = tk.Entry(pencere)
    entry_kategori.grid(row=4, column=1)

    tk.Button(pencere, text="Ekle", command=ekle).grid(row=5, column=1)

def kitaplari_listele_gui():
    conn = get_connection()
    if conn:
        kitaplar = kitaplari_listele(conn)
        conn.close()

        pencere = tk.Toplevel(root)
        pencere.title("Kitap Listesi")

        tree = ttk.Treeview(pencere, columns=("ID", "Ad", "Yazar", "Yayınevi", "Yayın Yılı", "Kategori"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Ad", text="Kitap Adı")
        tree.heading("Yazar", text="Yazar")
        tree.heading("Yayın Yılı", text="Yayın Yılı")
        tree.heading("Kategori", text="Kategori")

        for kitap in kitaplar:
            tree.insert("", "end", values=(kitap[0], kitap[1], kitap[2], kitap[3], kitap[4], kitap[5]))

        tree.pack(fill="both", expand=True)


def uye_ekle_gui():
    def ekle():
        conn = get_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO uyeler (ad, soyad, email, telefon, kayit_tarihi) VALUES (%s, %s, %s, %s, %s)"
                    values = (entry_ad.get(), entry_soyad.get(), entry_email.get(), entry_tel.get(), entry_tarih.get())
                    cursor.execute(sql, values)
                    conn.commit()
                messagebox.showinfo("Başarılı", "Üye eklendi.")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
            finally:
                conn.close()

    pencere = tk.Toplevel(root)
    pencere.title("Üye Ekle")

    tk.Label(pencere, text="Ad").grid(row=0, column=0)
    entry_ad = tk.Entry(pencere)
    entry_ad.grid(row=0, column=1)

    tk.Label(pencere, text="Soyad").grid(row=1, column=0)
    entry_soyad = tk.Entry(pencere)
    entry_soyad.grid(row=1, column=1)

    tk.Label(pencere, text="Email").grid(row=2, column=0)
    entry_email = tk.Entry(pencere)
    entry_email.grid(row=2, column=1)

    tk.Label(pencere, text="Telefon").grid(row=3, column=0)
    entry_tel = tk.Entry(pencere)
    entry_tel.grid(row=3, column=1)

    tk.Label(pencere, text="Kayıt Tarihi (YYYY-AA-GG)").grid(row=4, column=0)
    entry_tarih = tk.Entry(pencere)
    entry_tarih.grid(row=4, column=1)

    tk.Button(pencere, text="Ekle", command=ekle).grid(row=5, column=1)

def uyeleri_listele_gui():
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM uyeler")
                uyeler = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Hata", str(e))
            return
        finally:
            conn.close()

        pencere = tk.Toplevel(root)
        pencere.title("Üye Listesi")

        tree = ttk.Treeview(pencere, columns=("ID", "Ad", "Soyad", "Email"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Ad", text="Ad")
        tree.heading("Soyad", text="Soyad")
        tree.heading("Email", text="Email")

        for uye in uyeler:
            tree.insert("", "end", values=(uye[0], uye[1], uye[2], uye[3]))

        tree.pack(fill="both", expand=True)

def kitap_odunc_ver_gui():
    def ver():
        conn = get_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO odunc_kayitlari (kitap_id, uye_id, odunc_tarihi, iade_tarihi) VALUES (%s, %s, %s, %s)"
                    values = (int(entry_kitap.get()), int(entry_uye.get()), entry_odunc.get(), entry_iade.get())
                    cursor.execute(sql, values)
                    cursor.execute("UPDATE kitaplar SET durum = 'oduncte' WHERE kitap_id = %s", (int(entry_kitap.get()),))
                    conn.commit()
                messagebox.showinfo("Başarılı", "Kitap ödünç verildi!")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
            finally:
                conn.close()

    pencere = tk.Toplevel(root)
    pencere.title("Kitap Ödünç Ver")

    tk.Label(pencere, text="Kitap ID").grid(row=0, column=0)
    entry_kitap = tk.Entry(pencere)
    entry_kitap.grid(row=0, column=1)

    tk.Label(pencere, text="Üye ID").grid(row=1, column=0)
    entry_uye = tk.Entry(pencere)
    entry_uye.grid(row=1, column=1)

    tk.Label(pencere, text="Ödünç Tarihi (YYYY-AA-GG)").grid(row=2, column=0)
    entry_odunc = tk.Entry(pencere)
    entry_odunc.grid(row=2, column=1)

    tk.Label(pencere, text="İade Tarihi (YYYY-AA-GG)").grid(row=3, column=0)
    entry_iade = tk.Entry(pencere)
    entry_iade.grid(row=3, column=1)

    tk.Button(pencere, text="Ver", command=ver).grid(row=4, column=1)


def kitap_iade_gui():
    def iade_et():
        conn = get_connection()
        if conn:
            try:
                kitap_id = int(entry_id.get())
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE odunc_kayitlari SET teslim_edildi_mi = TRUE WHERE kitap_id = %s AND teslim_edildi_mi = FALSE", (kitap_id,))
                    cursor.execute("UPDATE kitaplar SET durum = 'mevcut' WHERE kitap_id = %s", (kitap_id,))
                    conn.commit()
                messagebox.showinfo("Başarılı", "Kitap iade edildi!")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
            finally:
                conn.close()

    pencere = tk.Toplevel(root)
    pencere.title("Kitap İade Et")

    tk.Label(pencere, text="Kitap ID").grid(row=0, column=0)
    entry_id = tk.Entry(pencere)
    entry_id.grid(row=0, column=1)

    tk.Button(pencere, text="İade Et", command=iade_et).grid(row=1, column=1)


root = tk.Tk()
root.title("Kütüphane Otomasyonu")

tk.Button(root, text="Kitap Ekle", width=100, command=kitap_ekle_gui).pack(pady=5, fill='x')
tk.Button(root, text="Kitapları Listele", width=100, command=kitaplari_listele_gui).pack(pady=5, fill='x')
tk.Button(root, text="Üye Ekle", width=100, command=uye_ekle_gui).pack(pady=5, fill='x')
tk.Button(root, text="Üyeleri Listele", width=100, command=uyeleri_listele_gui).pack(pady=5, fill='x')
tk.Button(root, text="Kitap Ödünç Ver", width=100, command=kitap_odunc_ver_gui).pack(pady=5, fill='x')
tk.Button(root, text="Kitap İade Et", width=100, command=kitap_iade_gui).pack(pady=5, fill='x')

root.mainloop()
