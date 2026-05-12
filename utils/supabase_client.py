from supabase import create_client


# =====================================================
# SUPABASE CONFIG
# =====================================================

SUPABASE_URL = "ISI_SUPABASE_URL_KAMU"

SUPABASE_KEY = "ISI_SUPABASE_ANON_KEY_KAMU"


# =====================================================
# CLIENT
# =====================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)