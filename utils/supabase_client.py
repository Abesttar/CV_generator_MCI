from supabase import create_client


# =====================================================
# SUPABASE CONFIG
# =====================================================

SUPABASE_URL = "https://hzszcuuonqbmjlhflsqn.supabase.co"

SUPABASE_KEY = "sb_publishable_8cbRrHSs92NBYbEhT6CsXQ_eTBxkrZO"


# =====================================================
# CLIENT
# =====================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)