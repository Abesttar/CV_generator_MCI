from datetime import date

from utils.formatter import *
from utils.furigana import *
from utils.translator import *

print(format_japanese_date(date.today()))

print(calculate_age(date(2000, 5, 8)))

print(format_phone("812345678"))

print(latin_to_katakana("Ahmad Rizki"))

print(
    translate_to_japanese(
        "Saya suka bekerja keras"
    )
)