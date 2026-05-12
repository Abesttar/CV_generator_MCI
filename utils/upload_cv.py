import os
from datetime import datetime

from utils.supabase_client import supabase


BUCKET_NAME = "cv-files"


# =====================================================
# UPLOAD FILE
# =====================================================

def upload_file(file_path, folder="cv"):

    if not os.path.exists(file_path):
        return None

    filename = os.path.basename(file_path)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    storage_path = (
        f"{folder}/"
        f"{timestamp}_{filename}"
    )

    with open(file_path, "rb") as f:

        supabase.storage.from_(
            BUCKET_NAME
        ).upload(
            storage_path,
            f,
            {
                "content-type":
                "application/octet-stream"
            }
        )

    public_url = supabase.storage.from_(
        BUCKET_NAME
    ).get_public_url(
        storage_path
    )

    return public_url


# =====================================================
# SAVE CV DATA
# =====================================================

def save_cv_data(
    nama,
    nomor,
    alamat,
    phone,
    excel_url,
    pdf_url
):

    data = {

        "nama": nama,

        "nomor": nomor,

        "excel_url": excel_url,

        "pdf_url": pdf_url,
    }

    response = supabase.table(
        "cvs"
    ).insert({

    "nama": nama,
    "nomor": nomor,
    "alamat": alamat,
    "phone": phone,
    "excel_url": excel_url,
    "pdf_url": pdf_url,

    }).execute()

    return response