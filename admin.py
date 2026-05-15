import streamlit as st
import requests
import re

from utils.supabase_client import supabase


# ====================================================
# CONFIG
# ====================================================

st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide"
)

# ====================================================
# LOGIN DATA
# ====================================================

ACCOUNTS = {

    "dokumen.mci": "mci2024",
    "admin.mci": "mci2024",
}

# ====================================================
# SESSION
# ====================================================

if "admin_login" not in st.session_state:

    st.session_state.admin_login = False

if "admin_username" not in st.session_state:

    st.session_state.admin_username = ""

# ====================================================
# SAFE FILE NAME
# ====================================================

def safe_filename(name):

    if not name:

        return "CV"

    name = name.upper()

    # hapus karakter aneh
    name = re.sub(
        r'[^A-Z0-9\s]',
        '',
        name
    )

    # ganti spasi jadi _
    name = re.sub(
        r'\s+',
        '_',
        name
    )

    return name.strip("_")


# ====================================================
# DOWNLOAD FILE
# ====================================================

def get_file_bytes(url):

    try:

        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code == 200:

            return response.content

    except:

        return None

    return None


# ====================================================
# LOGIN PAGE
# ====================================================

if not st.session_state.admin_login:

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🔐 Admin Login
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_btn = st.button(
            "Login",
            use_container_width=True
        )

        if login_btn:

            if (
                username in ACCOUNTS
                and
                ACCOUNTS[username] == password
            ):

                st.session_state.admin_login = True
                st.session_state.admin_username = username

                st.rerun()

            else:

                st.error(
                    "Username atau password salah"
                )

    st.stop()

# ====================================================
# HEADER
# ====================================================

col1, col2 = st.columns([6,1])

with col1:

    st.title("📄 Admin Dashboard CV")

    st.caption(
        f"Login sebagai: "
        f"{st.session_state.admin_username}"
    )

with col2:

    st.write("")

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.admin_login = False
        st.session_state.admin_username = ""

        st.rerun()

# ====================================================
# LOAD DATA
# ====================================================

response = supabase.table(
    "cvs"
).select("*").order(
    "created_at",
    desc=True
).execute()

cv_list = response.data

# ====================================================
# SEARCH + STATS
# ====================================================

col1, col2 = st.columns([3,1])

with col1:

    search = st.text_input(
        "Cari Nama"
    )

with col2:

    st.metric(
        "Total CV",
        len(cv_list)
    )

# ====================================================
# FILTER SEARCH
# ====================================================

if search:

    cv_list = [

        cv for cv in cv_list

        if search.lower()
        in cv.get(
            "nama",
            ""
        ).lower()
    ]

# ====================================================
# EMPTY DATA
# ====================================================

if not cv_list:

    st.warning(
        "Data CV tidak ditemukan"
    )

# ====================================================
# LIST CV
# ====================================================

for cv in cv_list:

    with st.container(border=True):

        col1, col2 = st.columns(
            [5,2]
        )

        nama_cv = cv.get(
            "nama",
            "CV"
        )

        safe_name = safe_filename(
            nama_cv
        )

        with col1:

            st.subheader(
                nama_cv
            )

            st.caption(
                cv.get(
                    "created_at",
                    "-"
                )
            )

            nomor = cv.get(
                "nomor",
                "-"
            )

            st.write(
                f"🆔 No CV: {nomor}"
            )

            st.write(
                f"📍 {cv.get('alamat', '-')}"
            )

            st.write(
                f"📞 {cv.get('phone', '-')}"
            )

        with col2:

            excel_url = cv.get(
                "excel_url"
            )

            pdf_url = cv.get(
                "pdf_url"
            )

            # =========================================
            # EXCEL DOWNLOAD
            # =========================================

            if excel_url:

                excel_bytes = get_file_bytes(
                    excel_url
                )

                if excel_bytes:

                    st.download_button(
                        label="📗 Download Excel",
                        data=excel_bytes,
                        file_name=f"CV_{safe_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key=f"excel_{nomor}"
                    )

            # =========================================
            # PDF DOWNLOAD
            # =========================================

            if pdf_url:

                pdf_bytes = get_file_bytes(
                    pdf_url
                )

                if pdf_bytes:

                    st.download_button(
                        label="📕 Download PDF",
                        data=pdf_bytes,
                        file_name=f"CV_{safe_name}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"pdf_{nomor}"
                    )

        st.divider()