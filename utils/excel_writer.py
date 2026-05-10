from openpyxl import load_workbook
from openpyxl.drawing.image import Image

from PIL import Image as PILImage

import os


TEMPLATE_PATH = "template/template_cv.xlsx"


FIELD_MAP = {

    "nomor": "C2",
    "tanggal_cv": "P3",
    "furigana": "F5",
    "nama": "F6",
    "alamat": "F7",
    "tanggal_lahir": "F8",
    "usia": "K8",
    "gender": "N8",
    "phone": "F9",
    "agama": "K9",
    "tinggi": "N9",
    "gol_darah": "F10",
    "status": "I10",
    "anak": "L10",
    "berat": "N10",
    "paspor": "R10",

    "pernah_jepang": "M25",
    "negara_lain": "M26",

    "kontak_nama": "G36",
    "kontak_hubungan": "K36",
    "kontak_nomor": "N36",

    "alasan": "F38",
    "hobi": "F40",
    "keahlian": "M40",
    "kelebihan": "F41",
    "kekurangan": "M41",
    "lainnya": "K42",

    "jp_duration": "I25",
    "jp_unit": "J25",
    "bahasa": "F26",
    "level_bahasa": "I26",
    "bahasa_unit": "J26",
}


PENDIDIKAN_ROWS = {
    0: 12,
    1: 13,
    2: 14,
    3: 15,
}

PENGALAMAN_ROWS = {
    0: 17,
    1: 19,
    2: 21,
    3: 23,
}

KELUARGA_ROWS = {
    0: 29,
    1: 30,
    2: 31,
    3: 32,
    4: 33,
    5: 34,
    6: 35,
}


def safe_year(value):

    if value:
        return f"{value}年"

    return ""


def safe_month(value):

    if value:
        return f"{value}月"

    return ""


def generate_cv(data):

    os.makedirs("output", exist_ok=True)

    wb = load_workbook(TEMPLATE_PATH)

    ws = wb["NAMA"]

    # =================================================
    # FIELD
    # =================================================

    for key, cell in FIELD_MAP.items():

        ws[cell] = data.get(key, "")

    # =================================================
    # HAPUS FOTO TEMPLATE
    # =================================================

    ws._images = []

    # =================================================
    # FOTO AUTO FIT
    # =================================================

    foto = data.get("foto")

    if foto:

        temp_path = "output/temp_photo.png"

        final_path = "output/final_photo.png"

        with open(temp_path, "wb") as f:

            f.write(foto.read())

        pil_img = PILImage.open(temp_path)

        if pil_img.mode != "RGB":

            pil_img = pil_img.convert("RGB")

        # =================================================
        # UKURAN FOTO FINAL
        # =================================================
        # sebelumnya terlalu besar
        # ini sudah diperkecil sedikit agar pas
        # =================================================

        FRAME_WIDTH = 145
        FRAME_HEIGHT = 200

        img_width, img_height = pil_img.size

        img_ratio = img_width / img_height

        frame_ratio = FRAME_WIDTH / FRAME_HEIGHT

        # =================================================
        # CROP AUTO TENGAH
        # =================================================

        if img_ratio > frame_ratio:

            new_width = int(img_height * frame_ratio)

            left = (img_width - new_width) // 2

            pil_img = pil_img.crop(
                (
                    left,
                    0,
                    left + new_width,
                    img_height
                )
            )

        else:

            new_height = int(img_width / frame_ratio)

            top = (img_height - new_height) // 2

            pil_img = pil_img.crop(
                (
                    0,
                    top,
                    img_width,
                    top + new_height
                )
            )

        # =================================================
        # RESIZE
        # =================================================

        pil_img = pil_img.resize(
            (
                FRAME_WIDTH,
                FRAME_HEIGHT
            )
        )

        pil_img.save(final_path)

        excel_img = Image(final_path)

        excel_img.width = FRAME_WIDTH
        excel_img.height = FRAME_HEIGHT

        # =================================================
        # TARUH FOTO
        # =================================================

        ws.add_image(excel_img, "P5")

    # =================================================
    # PENDIDIKAN
    # =================================================

    for index, item in enumerate(data.get("pendidikan", [])):

        if index not in PENDIDIKAN_ROWS:
            continue

        row = PENDIDIKAN_ROWS[index]

        ws[f"F{row}"] = safe_year(
            item.get("tahun_mulai")
        )

        ws[f"G{row}"] = safe_month(
            item.get("bulan_mulai")
        )

        ws[f"I{row}"] = safe_year(
            item.get("tahun_selesai")
        )

        ws[f"J{row}"] = safe_month(
            item.get("bulan_selesai")
        )

        level = item.get("level")

        if level == "SD":

            ws[f"K{row}"] = "小学生\nSD"

        elif level == "SMP":

            ws[f"K{row}"] = "中学生\nSMP"

        else:

            ws[f"K{row}"] = item.get(
                "level_jp",
                ""
            )

        ws[f"L{row}"] = item.get(
            "sekolah",
            ""
        )

        if row >= 14:

            ws[f"Q{row}"] = item.get(
                "jurusan",
                ""
            )

    # =================================================
    # PENGALAMAN
    # =================================================

    for index, item in enumerate(data.get("pengalaman", [])):

        if index not in PENGALAMAN_ROWS:
            continue

        row = PENGALAMAN_ROWS[index]

        ws[f"F{row}"] = safe_year(
            item.get("tm")
        )

        ws[f"G{row}"] = safe_month(
            item.get("bm")
        )

        ws[f"H{row}"] = item.get(
            "perusahaan",
            ""
        )

        ws[f"L{row}"] = item.get(
            "upah",
            ""
        )

        ws[f"N{row}"] = item.get(
            "pekerjaan",
            ""
        )

        ws[f"Q{row}"] = item.get(
            "posisi",
            ""
        )

    # =================================================
    # RIWAYAT JEPANG
    # =================================================

    if data.get("japan_tm"):

        ws["N25"] = (

            f'{data.get("japan_tm")}年 '

            f'{data.get("japan_bm")}月 ～ '

            f'{data.get("japan_ts")}年 '

            f'{data.get("japan_bs")}月'
        )

    # =================================================
    # NEGARA LAIN
    # =================================================

    negara_nama = data.get(
        "negara_nama",
        ""
    )

    if negara_nama:

        ws["N26"] = f'({negara_nama} 国)'

    # =================================================
    # KELUARGA
    # =================================================

    for index, item in enumerate(data.get("keluarga", [])):

        if index not in KELUARGA_ROWS:
            continue

        row = KELUARGA_ROWS[index]

        ws[f"B{row}"] = item.get(
            "hubungan",
            ""
        )

        ws[f"D{row}"] = item.get(
            "nama",
            ""
        )

        ws[f"I{row}"] = item.get(
            "usia",
            ""
        )

        ws[f"K{row}"] = item.get(
            "pekerjaan",
            ""
        )

    # =================================================
    # SAVE
    # =================================================

    output_path = "output/cv_jepang.xlsx"

    wb.save(output_path)

    return output_path