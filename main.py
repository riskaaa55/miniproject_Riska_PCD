import os
import cv2
import numpy as np
import pandas as pd

IMAGE_DIR = "data/images"
ABSENT_DIR = "data/test_absent"
RESULT_DIR = "results"
GLOBAL_DIR = os.path.join(RESULT_DIR, "global")
OTSU_DIR = os.path.join(RESULT_DIR, "otsu")

# ROI: area tanda tangan pada dokumen yang digunakan
Y1, Y2 = 0.12, 0.38
X1, X2 = 0.62, 0.95
GLOBAL_THRESHOLD = 180
SIGNATURE_RATIO_THRESHOLD = 0.03  # 3% foreground area
KERNEL = np.ones((3, 3), np.uint8)


def list_images(folder):
    return sorted([os.path.join(folder, f) for f in os.listdir(folder)
                   if f.lower().endswith((".jpg", ".jpeg", ".png"))])


def process(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Gagal membaca gambar: {path}")
    h, w = img.shape[:2]
    roi = img[int(h*Y1):int(h*Y2), int(w*X1):int(w*X2)]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, global_th = cv2.threshold(gray, GLOBAL_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    _, otsu_th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    def clean(binary):
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, KERNEL)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, KERNEL)
        return closing

    global_clean = clean(global_th)
    otsu_clean = clean(otsu_th)

    total = otsu_clean.size
    global_pixels = int(cv2.countNonZero(global_clean))
    otsu_pixels = int(cv2.countNonZero(otsu_clean))
    global_ratio = global_pixels / total
    otsu_ratio = otsu_pixels / total
    status = "SIGNATURE PRESENT" if otsu_ratio > SIGNATURE_RATIO_THRESHOLD else "SIGNATURE ABSENT"

    return roi, gray, global_clean, otsu_clean, global_pixels, otsu_pixels, global_ratio, otsu_ratio, status


def main():
    os.makedirs(GLOBAL_DIR, exist_ok=True)
    os.makedirs(OTSU_DIR, exist_ok=True)
    rows=[]
    samples=[]
    for label, folder in [("PRESENT", IMAGE_DIR), ("ABSENT", ABSENT_DIR)]:
        for path in list_images(folder):
            samples.append((path, label))

    if not samples:
        raise FileNotFoundError("Tidak ada citra pada data/images atau data/test_absent.")

    for path, true_label in samples:
        roi, gray, global_clean, otsu_clean, gp, op, gr, oratio, status = process(path)
        base=os.path.splitext(os.path.basename(path))[0]
        cv2.imwrite(os.path.join(GLOBAL_DIR, base+"_global.png"), global_clean)
        cv2.imwrite(os.path.join(OTSU_DIR, base+"_otsu.png"), otsu_clean)
        rows.append({
            "File": os.path.basename(path),
            "Data": true_label,
            "Global_Foreground_Pixels": gp,
            "Global_Foreground_Ratio": round(gr, 4),
            "Otsu_Foreground_Pixels": op,
            "Otsu_Foreground_Ratio": round(oratio, 4),
            "Detection": status,
            "Correct": status == ("SIGNATURE PRESENT" if true_label == "PRESENT" else "SIGNATURE ABSENT")
        })

    df=pd.DataFrame(rows)
    df.to_csv(os.path.join(RESULT_DIR,"detection_results.csv"), index=False)
    print("Hasil tersimpan di results/detection_results.csv")
    print(df.to_string(index=False))
    print("\nAkurasi:", f"{df['Correct'].mean()*100:.2f}%")

if __name__ == "__main__":
    main()
