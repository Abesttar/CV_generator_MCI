from deep_translator import GoogleTranslator
import re


# =====================================================
# CUSTOM TRANSLATION
# =====================================================

CUSTOM_TRANSLATIONS = {

    # pekerjaan
    "buruh": "工場作業員",
    "buruh pabrik": "工場作業員",
    "karyawan": "会社員",
    "admin": "事務員",
    "operator": "機械オペレーター",
    "staff": "スタッフ",
    "pelayan": "飲食店スタッフ",
    "kasir": "レジ係",
    "supir": "運転手",
    "driver": "運転手",
    "satpam": "警備員",
    "security": "警備員",
    "guru": "教師",
    "petani": "農業",
    "nelayan": "漁業",
    "ibu rumah tangga": "主婦",
    "wirausaha": "自営業",

    # sifat
    "jujur": "正直",
    "disiplin": "規律を守れます",
    "rajin": "真面目",
    "bertanggung jawab": "責任感があります",
    "cepat belajar": "覚えるのが早いです",

    # hobi
    "memasak": "料理",
    "olahraga": "スポーツ",
    "mancing": "釣り",
    "musik": "音楽",

    # skill
    "mengemudi": "運転できます",
    "komputer": "パソコン操作できます",
    "las": "溶接できます",
    "menjahit": "裁縫できます",
}


# =====================================================
# DETECT JAPANESE
# =====================================================

def contains_japanese(text):

    pattern = re.compile(
        r'[\u3040-\u30ff\u4e00-\u9faf]'
    )

    return bool(pattern.search(text))


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# NORMALIZE JAPANESE (N4 STYLE)
# =====================================================

def normalize_japanese(text):

    replacements = {

        # dictionary -> polite
        "できる": "できます",
        "わかる": "わかります",
        "分かる": "分かります",
        "話す": "話します",
        "読む": "読みます",
        "書く": "書きます",
        "行く": "行きます",
        "来る": "来ます",
        "食べる": "食べます",
        "見る": "見ます",
        "使う": "使います",
        "学ぶ": "学びます",
        "働く": "働きます",

        # casual -> polite
        "好きだ": "好きです",
        "得意だ": "得意です",

        # casual forms
        "してる": "しています",
        "やってる": "やっています",

        # cleaner CV wording
        "ことができます": "できます",

        # typo cleaner
        "ですです": "です",
        "ますます": "ます",

        # N4 common kanji
        "にほん": "日本",
        "にほんご": "日本語",
        "がっこう": "学校",
        "かいしゃ": "会社",
        "べんきょう": "勉強",
        "しごと": "仕事",
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    return text


# =====================================================
# ENSURE POLITE
# hanya untuk field tertentu
# =====================================================

def ensure_polite(text):

    text = text.strip()

    polite_endings = (
        "です",
        "ます",
        "ません",
        "ました",
        "できます",
        "あります",
    )

    if text.endswith(polite_endings):

        return text

    return text + "です"


# =====================================================
# MAIN TRANSLATOR
# =====================================================

def translate_to_japanese(
    text,
    formal=False
):

    if not text:

        return ""

    text = clean_text(text)

    lower_text = text.lower()

    # =================================================
    # CUSTOM TRANSLATION
    # =================================================

    if lower_text in CUSTOM_TRANSLATIONS:

        result = CUSTOM_TRANSLATIONS[
            lower_text
        ]

        if formal:
            result = ensure_polite(result)

        return result

    try:

        # =================================================
        # INPUT SUDAH JEPANG
        # =================================================

        if contains_japanese(text):

            result = normalize_japanese(
                text
            )

            if formal:
                result = ensure_polite(
                    result
                )

            return result

        # =================================================
        # INDONESIA -> JEPANG
        # =================================================

        result = GoogleTranslator(
            source="id",
            target="ja"
        ).translate(text)

        result = normalize_japanese(
            result
        )

        if formal:
            result = ensure_polite(
                result
            )

        return result

    except:

        return text