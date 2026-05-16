import streamlit as st
import requests
import base64
from datetime import date

from utils.formatter import (
    format_japanese_date,
    calculate_age,
    format_phone,
)

from utils.furigana import (
    latin_to_katakana
)

from utils.translator import (
    translate_to_japanese
)

from utils.excel_writer import (
    generate_cv
)

from utils.pdf_export import (
    convert_to_pdf
)

from utils.upload_cv import (
    upload_file,
    save_cv_data
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="CV Generator Jepang",
    layout="wide"
)

st.title("CV Generator Jepang")


YEARS = [""] + list(range(1985, 2027))
MONTHS = [""] + list(range(1, 13))

UPAH_LIST = [
    "なし",

    "10000円",
    "15000円",
    "20000円",
    "25000円",
    "30000円",
    "35000円",
    "40000円",
    "45000円",
    "50000円",
    "55000円",
    "60000円",
    "65000円",
    "70000円",
    "75000円",
    "80000円",
    "85000円",
    "90000円",
    "95000円",
    "100000円",
    "150000円",
    "200000円",
    "250000円",
    "300000円",
    "350000円",
]



# =====================================================
# API HELPERS
# =====================================================

BASE_API = "https://www.emsifa.com/api-wilayah-indonesia/api"


@st.cache_data
def get_provinces():

    url = f"{BASE_API}/provinces.json"

    return requests.get(url).json()


@st.cache_data
def get_regencies(province_id):

    url = (
        f"{BASE_API}/regencies/"
        f"{province_id}.json"
    )

    return requests.get(url).json()


@st.cache_data
def get_districts(regency_id):

    url = (
        f"{BASE_API}/districts/"
        f"{regency_id}.json"
    )

    return requests.get(url).json()


@st.cache_data
def get_villages(district_id):

    url = (
        f"{BASE_API}/villages/"
        f"{district_id}.json"
    )

    return requests.get(url).json()



# =====================================================
# HITUNG USIA
# =====================================================

def calculate_age(birth_date):

    today = date.today()

    return (
        today.year
        - birth_date.year
        - (
            (
                today.month,
                today.day
            )
            <
            (
                birth_date.month,
                birth_date.day
            )
        )
    )

# =====================================================
# AUTO UPPERCASE
# =====================================================

def to_upper(value):

    if not value:
        return ""

    return str(value).upper()

# =====================================================
# BIODATA
# =====================================================

st.header("Biodata")

col1, col2 = st.columns(2)

# =====================================================
# KOLOM KIRI
# =====================================================

with col1:

    nomor = st.text_input("No.")

    tanggal_cv = st.date_input(
        "Tanggal Pembuatan CV",
        value=date.today()
    )

    nama = to_upper(
    st.text_input(
        "Nama Alphabet"
    )
    )

    furigana = latin_to_katakana(
        nama
    )

    st.text_input(
        "Furigana",
        value=furigana,
        disabled=True
    )

    foto = st.file_uploader(
        "Upload Foto",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    jalan = to_upper(
    st.text_input(
        "Jalan"
    )
)

    kampung = to_upper(
    st.text_input(
        "Kampung"
    )
)

# =====================================================
# KOLOM KANAN
# =====================================================

with col2:

    # =========================================
    # NEGARA FIX
    # =========================================

    negara = "INDONESIA"

    st.text_input(
        "Negara",
        value=negara,
        disabled=True
    )

    # =========================================
    # PROVINSI
    # =========================================

    provinces = get_provinces()

    province_options = {
        p["name"]: p["id"]
        for p in provinces
    }

    selected_province = st.selectbox(
        "Provinsi",
        [""] + list(province_options.keys())
    )

    province_id = province_options.get(
        selected_province
    )

    # =========================================
    # KABUPATEN
    # =========================================

    selected_regency = ""

    regency_id = None

    if province_id:

        regencies = get_regencies(
            province_id
        )

        regency_options = {
            r["name"]: r["id"]
            for r in regencies
        }

        selected_regency = st.selectbox(
            "Kabupaten / Kota",
            [""] + list(
                regency_options.keys()
            )
        )

        regency_id = regency_options.get(
            selected_regency
        )

    # =========================================
    # KECAMATAN
    # =========================================

    selected_district = ""

    district_id = None

    if regency_id:

        districts = get_districts(
            regency_id
        )

        district_options = {
            d["name"]: d["id"]
            for d in districts
        }

        selected_district = st.selectbox(
            "Kecamatan",
            [""] + list(
                district_options.keys()
            )
        )

        district_id = district_options.get(
            selected_district
        )

    # =========================================
    # DESA
    # =========================================

    selected_village = ""

    if district_id:

        villages = get_villages(
            district_id
        )

        village_options = [
            v["name"]
            for v in villages
        ]

        selected_village = st.selectbox(
            "Desa / Kelurahan",
            [""] + village_options
        )

    # =========================================
    # KODE POS MANUAL
    # =========================================

    kode_pos = st.text_input(
    "Kode Pos"
    )

    # =========================================
    # TANGGAL LAHIR
    # =========================================

    tanggal_lahir = st.date_input(
        "Tanggal Lahir",
        value=date(
            2000,
            1,
            1
        ),
        min_value=date(
            1980,
            1,
            1
        ),
        max_value=date(
            2020,
            12,
            31
        )
    )

    usia = calculate_age(
        tanggal_lahir
    )

    st.text_input(
        "Usia",
        value=str(usia),
        disabled=True
    )

    # =========================================
    # GENDER
    # =========================================

    gender = st.selectbox(
        "Jenis Kelamin",
        [
            "",
            "男            PRIA",
            "女            WANITA"
        ],
        index=0
    )

# =====================================================
# FINAL ALAMAT
# =====================================================

alamat_parts = [

    jalan,
    kampung,
    selected_village,
    selected_district,
    selected_regency,
]

alamat_parts = [
    x for x in alamat_parts
    if x
]

alamat = ", ".join(
    alamat_parts
)

if kode_pos:

    alamat += f" - {kode_pos}"

if selected_province:

    alamat += f", {selected_province}"

alamat += ", INDONESIA"


# =====================================================
# KONTAK
# =====================================================

st.header("Kontak")

col1, col2, col3 = st.columns(3)

with col1:

    phone_input = st.text_input(
        "Nomor Telepon",
        placeholder="812345678"
    )

    phone = format_phone(
        phone_input
    )

with col2:

    agama = st.selectbox(
        "Agama",
        [
            "イスラム教　   ISLAM",
            "キリスト教   KRISTEN",
            "カトリック    KATOLIK",
            "ヒンドゥー教  HINDU",
            "仏教          BUDDHA"
        ]
    )

with col3:

    gol_darah = st.selectbox(
        "Golongan Darah",
        [
            "A型",
            "B型",
            "O型",
            "AB型"
        ]
    )

col1, col2, col3, col4 = st.columns(4)

with col1:

    tinggi = st.text_input(
        "Tinggi Badan"
    )

with col2:

    status = st.selectbox(
        "Status",
        [
            "未婚 SINGLE",
            "既婚 MENIKAH",
            "離婚 CERAI"
        ]
    )

with col3:

    anak = st.selectbox(
        "Anak",
        [
            "無 　TIDAK",
            "1",
            "2",
            "3",
            "4",
            "5"
        ]
    )

with col4:

    berat = st.text_input(
        "Berat Badan"
    )

paspor = st.selectbox(
    "Paspor",
    [
        "有      ADA",
        "無      TIDAK"
    ]
)


# =====================================================
# PENDIDIKAN
# =====================================================

st.header("Pendidikan")

pendidikan_list = []

levels = [
    "SD",
    "SMP",
    "SMA",
    "Kuliah"
]

for level in levels:

    with st.expander(level):

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            tahun_mulai = st.selectbox(
                "Tahun Mulai",
                [""] + YEARS,
                index=0,
                key=f"tm_{level}"
            )

        with col2:

            bulan_mulai = st.selectbox(
                "Bulan Mulai",
                [""] + MONTHS,
                index=0,
                key=f"bm_{level}"
            )

        with col3:

            tahun_selesai = st.selectbox(
                "Tahun Selesai",
                [""] + YEARS,
                index=0,
                key=f"ts_{level}"
            )

        with col4:

            bulan_selesai = st.selectbox(
                "Bulan Selesai",
                [""] + MONTHS,
                index=0,
                key=f"bs_{level}"
            )

        # =========================================
        # LEVEL SEKOLAH
        # =========================================

        if level == "SMA":

            level_jp = st.selectbox(
                "Level SMA",
                [
                    "",
                    "普通高校　SMA",
                    "職業高校　SMK",
                    "単位高校　PaketC"
                ],
                index=0,
                key="sma_level"
            )

        elif level == "Kuliah":

            level_jp = st.selectbox(
                "Level Kuliah",
                [
                    "",
                    "4年制大学D4・S1",
                    "3年制大学D3"
                ],
                index=0,
                key="kuliah_level"
            )

        else:
            level_jp = level

        # =========================================
        # NAMA SEKOLAH
        # =========================================

        sekolah = to_upper(
        st.text_input(
        "Nama Sekolah",
        key=f"sekolah_{level}"
            )
        )

        # =========================================
        # JURUSAN
        # =========================================

        jurusan = to_upper(
        st.text_input(
        "Jurusan",
        key=f"jurusan_{level}"
            )
        )

        pendidikan_list.append({

            "level": level,

            "level_jp": level_jp,

            "tahun_mulai": tahun_mulai,

            "bulan_mulai": bulan_mulai,

            "tahun_selesai": tahun_selesai,

            "bulan_selesai": bulan_selesai,

            "sekolah": sekolah,

            "jurusan": jurusan,
        })

# =====================================================
# PENGALAMAN KERJA
# =====================================================

st.header("Pengalaman Kerja")

pengalaman_list = []

for i in range(1, 5):

    with st.expander(f"Pengalaman Kerja {i}"):

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            tm = st.selectbox(
                "Tahun Mulai",
                YEARS,
                index=0,
                key=f"pktm{i}"
            )

        with col2:

            bm = st.selectbox(
                "Bulan Mulai",
                MONTHS,
                index=0,
                key=f"pkbm{i}"
            )

        with col3:

            ts = st.selectbox(
                "Tahun Selesai",
                YEARS,
                index=0,
                key=f"pkts{i}"
            )

        with col4:

            bs = st.selectbox(
                "Bulan Selesai",
                MONTHS,
                index=0,
                key=f"pkbs{i}"
            )

        perusahaan = to_upper(
        st.text_input(
        "Nama Perusahaan",
        key=f"perusahaan{i}"
             )
        )

        # =========================================
        # UPAH DEFAULT KOSONG
        # =========================================

        upah = st.selectbox(
            "Upah Bulanan",
            [""] + UPAH_LIST,
            index=0,
            key=f"upah{i}"
        )

        pekerjaan = st.text_input(
            "Jenis Pekerjaan",
            key=f"pekerjaan{i}"
        )

        pekerjaan_jp = translate_to_japanese(
            pekerjaan,
            formal=False
        )

        # =========================================
        # POSISI DEFAULT KOSONG
        # =========================================

        posisi = st.selectbox(
            "Posisi",
            [
                "",
                "契約社員 Karyawan kontrak",
                "正社員 Karyawan tetap",
                "アルバイト Part Time"
            ],
            index=0,
            key=f"posisi{i}"
        )

        pengalaman_list.append({

            "tm": tm,
            "bm": bm,
            "ts": ts,
            "bs": bs,

            "perusahaan": perusahaan,

            "upah": upah,

            "pekerjaan": pekerjaan_jp,

            "posisi": posisi,
        })
# =====================================================
# BAHASA ASING
# =====================================================

st.header("Bahasa Asing")

col1, col2, col3 = st.columns(3)

with col1:

    jp_duration = st.selectbox(
        "日本語学習期間",
        [""] + list(range(1, 21)),
        index=0
    )

with col2:

    jp_unit = st.selectbox(
        "Satuan Belajar Jepang",
        [
            "",
            "ヶ月",
            "週間",
            "年間"
        ],
        index=0
    )

with col3:

    st.empty()

col1, col2, col3 = st.columns(3)

with col1:

    bahasa = st.selectbox(
        "Bahasa Asing",
        [
            "",
            "英語",
            "韓国語",
            "中国語",
            "アラビア語",
            "ドイツ語",
            "フランス語",
            "台湾語",
            "ベトナム語",
            "タイ語",
            "スペイン語"
        ],
        index=0
    )

with col2:

    level_bahasa = st.selectbox(
        "Level",
        [
            "",
            "初級",
            "中級",
            "上級"
        ],
        index=0
    )

with col3:

    bahasa_unit = st.selectbox(
        "Satuan",
        [
            "",
            "ヶ月",
            "週間",
            "年間"
        ],
        index=0
    )

# =====================================================
# PERNAH KE JEPANG
# =====================================================

st.header("Riwayat Jepang")

pernah_jepang = st.selectbox(
    "Pernah ke Jepang",
    [
        "",
        "有      ADA",
        "無 TIDAK"
    ],
    index=0
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    japan_tm = st.selectbox(
        "Tahun Mulai Jepang",
        [""] + YEARS,
        index=0
    )

with col2:

    japan_bm = st.selectbox(
        "Bulan Mulai Jepang",
        [""] + MONTHS,
        index=0
    )

with col3:

    japan_ts = st.selectbox(
        "Tahun Selesai Jepang",
        [""] + YEARS,
        index=0
    )

with col4:

    japan_bs = st.selectbox(
        "Bulan Selesai Jepang",
        [""] + MONTHS,
        index=0
    )


# =====================================================
# NEGARA LAIN
# =====================================================

st.header("Negara Lain")

negara_lain = st.selectbox(
    "Pernah ke Negara Lain",
    [
        "",
        "有      ADA",
        "無 TIDAK"
    ],
    index=0
)

negara_nama = st.text_input(
    "Nama Negara"
)
# =====================================================
# DATA KELUARGA
# =====================================================

st.header("Data Keluarga")

keluarga_list = []

for i in range(1, 8):

    with st.expander(f"Keluarga {i}"):

        hubungan = st.selectbox(
            "Hubungan",
            [
                "",
                "父 Ayah",
                "母 Ibu",
                "兄 Kakak laki-laki",
                "姉 Kakak perempuan",
                "弟 Adik laki-laki",
                "妹 Adik perempuan",
                "夫 Suami",
                "妻 Istri",
                "子 Anak",
                "祖父 Kakek",
                "祖母 Nenek",
                "おじ Paman",
                "おば Bibi",
            ],
            index=0,
            key=f"hubungan{i}"
        )

        nama_keluarga = to_upper(
         st.text_input(
        "Nama",
        key=f"nama_keluarga{i}"
             )
        )

        col_usia1, col_usia2 = st.columns(2)

    with col_usia1:

        usia_input = st.text_input(
        "Usia",
        key=f"usia_keluarga{i}"
    )

    with col_usia2:

        usia_satuan = st.selectbox(
        "Satuan",
        [
            "歳",
            "ヶ月"
        ],
        key=f"satuan_usia{i}"
        )

    usia_keluarga = ""

    if usia_input.strip():

        usia_keluarga = (
        f"{usia_input.strip()} "
        f"{usia_satuan}"
        )

        pekerjaan_keluarga = st.text_input(
            "Pekerjaan",
            key=f"pekerjaan_keluarga{i}"
        )

        pekerjaan_keluarga_jp = translate_to_japanese(
            pekerjaan_keluarga,
            formal=False
        )

        keluarga_list.append({
            "hubungan": hubungan,
            "nama": nama_keluarga,
            "usia": usia_keluarga,
            "pekerjaan": pekerjaan_keluarga_jp,
        })
# =====================================================
# KONTAK DARURAT
# =====================================================

st.header("Kontak Darurat")

col1, col2, col3 = st.columns(3)

with col1:

    kontak_nama = to_upper(
    st.text_input(
        "Nama Kontak"
         )
    )

with col2:

    kontak_hubungan = st.selectbox(
        "Hubungan",
        [
            "",
            "父 Ayah",
            "母 Ibu",
            "兄 Kakak laki-laki",
            "姉 Kakak perempuan",
            "弟 Adik laki-laki",
            "妹 Adik perempuan",
            "夫 Suami",
            "妻 Istri"
        ]
    )

with col3:

    kontak_nomor_input = st.text_input(
        "Nomor Kontak",
        placeholder="812345678"
    )

    kontak_nomor = format_phone(
        kontak_nomor_input
    )


# =====================================================
# TEXT AREA
# =====================================================

st.header("Informasi Tambahan")

alasan = st.text_area("Tujuan Bekerja ke Jepang")

hobi = st.text_area("Hobi")

keahlian = st.text_area("Keahlian Khusus")

kelebihan = st.text_area("Kelebihan")

kekurangan = st.text_area("Kekurangan")

# =====================================================
# KENDARAAN & SIM
# =====================================================

st.header("Kendaraan & SIM")

bisa_kendara = st.selectbox(
    "Bisa Berkendara",
    [
        "",
        "普通車 - Mobil",
        "軽自動車 - Mobil Kecil",
        "バイク - Motor",
        "大型バイク - Motor Besar",
        "トラック - Truk",
        "大型トラック - Truk Besar",
        "バス - Bus",
        "フォークリフト - Forklift",
        "ショベルカー - Excavator",
        "ブルドーザー - Bulldozer",
        "クレーン - Crane",
        "トラクター - Traktor",
        "両方 - Mobil & Motor",
        "その他 - Lainnya"
    ],
    index=0
)

# =====================================================
# INPUT MANUAL JIKA PILIH LAINNYA
# =====================================================

if bisa_kendara == "その他 - Lainnya":

    custom_kendara = st.text_input(
        "Isi Kendaraan Lainnya",
        placeholder="contoh: 救急車 - Ambulans"
    )

    bisa_kendara = custom_kendara

sim_1 = st.text_input("SIM 1")
sim_2 = st.text_input("SIM 2")
sim_3 = st.text_input("SIM 3")

# =====================================================
# GENERATE
# =====================================================

if st.button("Generate CV"):

    data = {

        "nomor": nomor,

        "tanggal_cv":
        format_japanese_date(tanggal_cv),

        "nama": nama,

        "furigana": furigana,

        "foto": foto,

        "alamat": alamat,

        "tanggal_lahir":
        format_japanese_date(
            tanggal_lahir
        ),

        "usia": usia,

        "gender": gender,

        "phone": phone,

        "agama": agama,

        "tinggi": tinggi,

        "gol_darah": gol_darah,

        "status": status,

        "anak": anak,

        "berat": berat,

        "paspor": paspor,

        "pendidikan":
        pendidikan_list,

        "pengalaman":
        pengalaman_list,

        "jp_duration": jp_duration,

        "jp_unit": jp_unit,

        "bahasa": bahasa,

        "level_bahasa": level_bahasa,

        "bahasa_unit": bahasa_unit,

        "pernah_jepang":
        pernah_jepang,

        "japan_tm":
        japan_tm,

        "japan_bm":
        japan_bm,

        "japan_ts":
        japan_ts,

        "japan_bs":
        japan_bs,

        "negara_lain":
        negara_lain,

        "negara_nama":
        negara_nama,

        "keluarga":
        keluarga_list,

        "kontak_nama":
        kontak_nama,

        "kontak_hubungan":
        kontak_hubungan,

        "kontak_nomor":
        kontak_nomor,

        "alasan":
        translate_to_japanese(
            alasan,
            formal=True
        ),

        "hobi":
        translate_to_japanese(
            hobi,
            formal=True
        ),

        "keahlian":
        translate_to_japanese(
            keahlian,
            formal=True
        ),

        "kelebihan":
        translate_to_japanese(
            kelebihan,
            formal=True
        ),

        "kekurangan":
        translate_to_japanese(
            kekurangan,
            formal=True
        ),

        "bisa_kendara":
        bisa_kendara,

        "sim_1":
        to_upper(sim_1),

        "sim_2":
        to_upper(sim_2),

        "sim_3":
        to_upper(sim_3),

        "sim_4":
        to_upper(sim_4),
    }

    excel_path = generate_cv(data)

    try:

        pdf_path = convert_to_pdf(
            excel_path
        )

        pdf_available = True

    except Exception:

        pdf_available = False

    st.success("CV berhasil dibuat")

    # =============================================
    # NAMA FILE OTOMATIS
    # =============================================

    safe_name = nama.strip().replace(" ", "_")

    if not safe_name:
        safe_name = "cv_jepang"

    excel_filename = f"CV_{safe_name}.xlsx"
    pdf_filename = f"CV_{safe_name}.pdf"



    # =============================================
    # UPLOAD EXCEL
    # =============================================

    excel_url = upload_file(
        excel_path,
        "excel"
    )

    pdf_url = None

    # =============================================
    # UPLOAD PDF
    # =============================================

    if pdf_available:

        pdf_url = upload_file(
            pdf_path,
            "pdf"
        )

    # =============================================
    # SAVE DATABASE
    # =============================================

    save_cv_data(

    nama=nama,

    nomor=nomor,

    alamat=alamat,

    phone=phone,

    excel_url=excel_url,

    pdf_url=pdf_url
    )

    st.success(
        "CV berhasil disimpan"
    )