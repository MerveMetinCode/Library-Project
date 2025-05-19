CREATE DATABASE kutuphane;
Use kutuphane;
CREATE TABLE kitaplar (
    kitap_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(100),
    yazar VARCHAR(100),
    yayinevi VARCHAR(100),
    yayin_yili INT,
    kategori VARCHAR(100),
    durum VARCHAR(20) DEFAULT 'mevcut'
);
Use kutuphane;
CREATE TABLE uyeler (
uye_id INT AUTO_INCREMENT PRIMARY KEY,
ad VARCHAR(100),
soyad VARCHAR(100),
email VARCHAR(100),
telefon VARCHAR(20),
kayit_tarihi DATE
);

Use kutuphane;
CREATE TABLE odunc_kayitlari (
kayit_id INT AUTO_INCREMENT PRIMARY KEY,
kitap_id INT,
uye_id INT,
odunc_tarihi DATE,
iade_tarihi DATE,
teslim_edildi_mi BOOLEAN DEFAULT FALSE,
FOREIGN KEY (kitap_id) REFERENCES kitaplar(kitap_id),
FOREIGN KEY (uye_id) REFERENCES uyeler(uye_id)
);