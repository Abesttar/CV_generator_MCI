import streamlit as st

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
]

JURUSAN_LIST = [
    "",
    "英語学科",
    "インドネシア語学科",
    "音楽科",
    "外国語学科",
    "観光学科",
    "看護学科",
    "機械学科",
    "機械整備学科",
    "漁業学科",
    "車、バイク整備学科",
    "経営学科",
    "経済学科",
    "芸能学科",
    "経理学科",
    "建築学科",
    "航海学科",
    "工業学科",
    "コンピューター学科",
    "裁縫学科",
    "情報学科",
    "助産師学科",
    "水産学科",
    "数学科",
    "ソフトウェア学科",
    "体育科",
    "畜産学科",
    "調理学科",
    "デザイン学科",
    "電気学科",
    "電子学科",
    "日本語学科",
    "農学科",
    "ビジネス学科",
    "福祉学科",
    "服飾科",
    "普通科",
    "文学科",
    "ホテル学科",
    "マネジメント学科",
    "マルチメディア学科",
    "薬学科",
    "養殖学科",
    "溶接学科",
]


# =====================================================
# BIODATA
# =====================================================

st.header("Biodata")

col1, col2 = st.columns(2)

with col1:

    nomor = st.text_input("No.")

    tanggal_cv = st.date_input(
        "Tanggal Pembuatan CV",
        value=date.today()
    )

    nama = st.text_input(
        "Nama Alphabet"
    )

    furigana = latin_to_katakana(nama)

    st.text_input(
        "Furigana",
        value=furigana,
        disabled=True
    )

    foto = st.file_uploader(
        "Upload Foto",
        type=["jpg", "jpeg", "png"]
    )

    jalan = st.text_input("Jalan")

    kampung = st.text_input("Kampung")

    desa = st.text_input("Desa")

with col2:

    kecamatan = st.text_input("Kecamatan")

    kabupaten = st.text_input("Kabupaten")

    kode_pos = st.text_input("Kode Pos")
    provinsi = st.text_input("Provinsi")

    negara = st.text_input(
    "Negara",
    value="Indonesia"
)

    tanggal_lahir = st.date_input(
    "Tanggal Lahir",
    value=date(2000, 1, 1),
    min_value=date(1980, 1, 1),
    max_value=date(2020, 12, 31)
)
    usia = calculate_age(
        tanggal_lahir
    )

    st.text_input(
        "Usia",
        value=str(usia),
        disabled=True
    )

    gender = st.selectbox(
        "Jenis Kelamin",
        [
            "男            Pria",
            "女            Wanita"
        ]
    )

alamat = (
    f"{jalan}, {kampung}, {desa}, "
    f"{kecamatan}, {kabupaten} - "
    f"{kode_pos}, {provinsi}, {negara}"
)


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
            "イスラム教　   Islam",
            "キリスト教    Kristen",
            "カトリック    Katolik",
            "ヒンドゥー教  Hindu",
            "仏教          Buddha"
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
            "未婚 Single",
            "既婚 Menikah",
            "離婚 Cerai"
        ]
    )

with col3:

    anak = st.selectbox(
        "Anak",
        [
            "無 　Tidak",
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
        "有      Ada",
        "無      Tidak"
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

        sekolah = st.text_input(
            "Nama Sekolah",
            key=f"sekolah_{level}"
        )

        # =========================================
        # JURUSAN
        # =========================================

        jurusan = st.selectbox(
            "Jurusan",
            JURUSAN_LIST,
            index=0,
            key=f"jurusan_{level}"
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

        perusahaan = st.text_input(
            "Nama Perusahaan",
            key=f"perusahaan{i}"
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
            pekerjaan
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
        "有      Ada",
        "無 Tidak"
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
        "有      Ada",
        "無 Tidak"
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
                "兄 Kakak cowo",
                "姉 Kakak cewe",
                "弟 Adik cowo",
                "妹 Adik cewe",
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

        nama_keluarga = st.text_input(
            "Nama",
            key=f"nama_keluarga{i}"
        )

        usia_input = st.text_input(
            "Usia",
            key=f"usia_keluarga{i}"
        )

        # =========================================
        # TAMBAH 歳 OTOMATIS
        # =========================================

        usia_keluarga = ""

        if usia_input.strip():

            usia_keluarga = f"{usia_input.strip()} 歳"

        pekerjaan_keluarga = st.text_input(
            "Pekerjaan",
            key=f"pekerjaan_keluarga{i}"
        )

        pekerjaan_keluarga_jp = translate_to_japanese(
            pekerjaan_keluarga
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

    kontak_nama = st.text_input(
        "Nama Kontak"
    )

with col2:

    kontak_hubungan = st.selectbox(
        "Hubungan",
            [
                "",
                "ちち",
                "はは",
                "あに",
                "あね",
                "おとうと",
                "いもうと",
                "おっと",
                "つま"
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

alasan = st.text_area("Alasan Melamar")

hobi = st.text_area("Hobi")

keahlian = st.text_area("Keahlian Khusus")

kelebihan = st.text_area("Kelebihan")

kekurangan = st.text_area("Kekurangan")

lainnya = st.text_area("Keterangan Lainnya")


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
            alasan
        ),

        "hobi":
        translate_to_japanese(
            hobi
        ),

        "keahlian":
        translate_to_japanese(
            keahlian
        ),

        "kelebihan":
        translate_to_japanese(
            kelebihan
        ),

        "kekurangan":
        translate_to_japanese(
            kekurangan
        ),

        "lainnya":
        translate_to_japanese(
            lainnya
        ),
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
    # DOWNLOAD EXCEL
    # =============================================

    with open(excel_path, "rb") as file:

        st.download_button(
            label="Download Excel",
            data=file,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # =============================================
    # DOWNLOAD PDF
    # =============================================

    if pdf_available:

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="Download PDF",
                data=file,
                file_name=pdf_filename,
                mime="application/pdf"
            )

    else:

        st.warning(
            "PDF export tidak tersedia di Streamlit Cloud"
        )