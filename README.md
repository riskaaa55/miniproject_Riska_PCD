# Signature Detection Miniproject

## Deskripsi

Miniproject ini mendeteksi keberadaan tanda tangan pada area tanda tangan dokumen. Tahapan yang digunakan adalah:

1. Crop area tanda tangan (ROI).
2. Konversi ROI menjadi grayscale.
3. Global thresholding.
4. Otsu thresholding.
5. Morphological opening dan closing.
6. Menghitung jumlah piksel foreground dan foreground ratio.
7. Menentukan `SIGNATURE PRESENT` atau `SIGNATURE ABSENT` menggunakan satu aturan keputusan yang sama.
8. Menguji citra yang memiliki tanda tangan dan citra tanpa tanda tangan.

## Struktur Folder

```text
signature_detection_final/
├── data/
│   ├── images/        # 9 citra dengan tanda tangan
│   └── test_absent/   # 5 citra tanpa tanda tangan (uji negatif terkontrol)
├── results/
├── main.py
├── signature_detection.ipynb
├── requirements.txt
└── README.md
```

> Catatan: citra pada `test_absent` dibuat sebagai sampel negatif terkontrol dengan mengosongkan area ROI tanda tangan dari beberapa dokumen uji. Tujuannya agar sistem dapat diuji pada kondisi `SIGNATURE ABSENT` ketika kumpulan citra awal hanya berisi citra bertanda tangan.

## How to Run

### Cara 1 — Menjalankan Python Script

1. Pastikan Python 3 sudah terpasang.
2. Buka terminal/CMD pada folder repository.
3. Install library:

```bash
pip install -r requirements.txt
```

4. Jalankan program:

```bash
python main.py
```

5. Hasil akan tersimpan pada folder `results/`, terutama:

```text
results/detection_results.csv
results/global/
results/otsu/
```

### Cara 2 — Menjalankan Jupyter Notebook

Install Jupyter jika belum ada:

```bash
pip install -r requirements.txt
```

Kemudian jalankan:

```bash
jupyter notebook
```

Buka file `signature_detection.ipynb`, lalu jalankan semua cell dari atas ke bawah.

### Cara 3 — Google Colab

1. Upload `signature_detection.ipynb` ke Google Colab.
2. Upload folder `data` ke `/content` sehingga struktur foldernya tetap sama.
3. Jalankan cell dari atas ke bawah.

## Metode Thresholding

### Global Threshold

Nilai ambang ditetapkan sebesar 180. Piksel yang lebih gelap dari ambang dianggap foreground setelah inverse threshold.

### Otsu Threshold

Nilai ambang ditentukan otomatis berdasarkan distribusi intensitas grayscale. Hasil Otsu digunakan sebagai dasar keputusan akhir karena dapat menyesuaikan ambang dengan karakteristik citra.

## Morphological Operation

- **Opening** mengurangi noise atau objek kecil.
- **Closing** membantu menyambungkan bagian foreground yang terputus.

## Aturan Keputusan

Foreground ratio dihitung dengan:

```text
foreground ratio = jumlah piksel foreground / jumlah seluruh piksel ROI
```

Aturan sederhana yang digunakan:

```text
Jika foreground ratio > 0.03
    SIGNATURE PRESENT
Jika foreground ratio <= 0.03
    SIGNATURE ABSENT
```

Nilai `0.03` berarti 3% area ROI menjadi foreground.

## Analisis

### Mengapa thresholding diperlukan?

Thresholding mengubah citra grayscale menjadi citra biner sehingga area gelap seperti goresan tanda tangan dapat dipisahkan dari background. Setelah menjadi biner, jumlah piksel foreground dapat dihitung secara kuantitatif untuk menentukan keberadaan tanda tangan.

### Apa masalah jika threshold terlalu tinggi atau terlalu rendah?

Jika threshold terlalu tinggi, terlalu banyak piksel dapat dianggap foreground sehingga background/noise ikut terdeteksi sebagai tanda tangan. Jika threshold terlalu rendah, bagian tanda tangan yang tipis atau samar dapat hilang sehingga jumlah foreground menjadi terlalu kecil dan tanda tangan berpotensi dianggap tidak ada.

## Output

Program menghasilkan tabel `detection_results.csv` yang berisi nama file, label data, jumlah piksel foreground, foreground ratio, hasil deteksi, dan apakah prediksi benar terhadap label pengujian.
