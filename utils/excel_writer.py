from openpyxl import load_workbook
from openpyxl.drawing.image import Image

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

    # BAHASA

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
    # FOTO
    # =================================================

    foto = data.get("foto")

    if foto:

        temp_path = "output/temp_photo.png"

        with open(temp_path, "wb") as f:
            f.write(foto.read())

        img = Image(temp_path)

        img.width = 115
        img.height = 145

        ws.add_image(img, "P5")

    # =================================================
    # PENDIDIKAN
    # =================================================

    for index, item in enumerate(
        data.get("pendidikan", [])
    ):

        if index not in PENDIDIKAN_ROWS:
            continue

        row = PENDIDIKAN_ROWS[index]

        ws[f"F{row}"] = f'{item["tahun_mulai"]}年'
        ws[f"G{row}"] = f'{item["bulan_mulai"]}月'

        ws[f"I{row}"] = f'{item["tahun_selesai"]}年'
        ws[f"J{row}"] = f'{item["bulan_selesai"]}月'

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

    for index, item in enumerate(
        data.get("pengalaman", [])
    ):

        if index not in PENGALAMAN_ROWS:
            continue

        row = PENGALAMAN_ROWS[index]

        ws[f"F{row}"] = f'{item["tm"]}年'

        ws[f"G{row}"] = f'{item["bm"]}月'

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

    ws["N26"] = f'({negara_nama} 国)'

    # =================================================
    # KELUARGA
    # =================================================

    for index, item in enumerate(
        data.get("keluarga", [])
    ):

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

    output_path = "output/cv_jepang.xlsx"

    wb.save(output_path)

    return output_path