import streamlit as st
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
            [5,1]
        )

        with col1:

            st.subheader(
                cv.get(
                    "nama",
                    "-"
                )
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

            if excel_url:

                st.link_button(
                    "📗 Excel",
                    excel_url,
                    use_container_width=True
                )

            if pdf_url:

                st.link_button(
                    "📕 PDF",
                    pdf_url,
                    use_container_width=True
                )

        st.divider()