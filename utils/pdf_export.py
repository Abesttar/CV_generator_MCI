import subprocess
from pathlib import Path


LIBREOFFICE_PATH = (
    "/Applications/LibreOffice.app/"
    "Contents/MacOS/soffice"
)


def convert_to_pdf(excel_path):

    output_dir = "output"

    subprocess.run([
        LIBREOFFICE_PATH,
        "--headless",
        "--convert-to",
        "pdf",
        excel_path,
        "--outdir",
        output_dir
    ])

    pdf_path = (
        Path(excel_path)
        .with_suffix(".pdf")
    )

    return str(pdf_path)