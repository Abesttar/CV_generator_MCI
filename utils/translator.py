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
    "jujur": "正直です",
    "disiplin": "規律を守れます",
    "rajin": "真面目です",
    "bertanggung jawab": "責任感があります",
    "cepat belajar": "覚えるのが早いです",

    # hobi
    "memasak": "料理です",
    "olahraga": "スポーツです",
    "mancing": "釣りです",
    "musik": "音楽です",

    # skill
    "mengemudi": "運転できます",
    "komputer": "パソコン操作できます",
    "las": "溶接できます",
    "menjahit": "裁縫できます",
}


# =====================================================
# ROMAJI -> JAPANESE
# =====================================================

ROMAJI_MAP = {

    "watashi": "私",
    "boku": "僕",
    "ore": "私",

    "nihongo": "日本語",
    "nihon": "日本",
    "kaisha": "会社",
    "gakkou": "学校",
    "sensei": "先生",

    "dekiru": "できます",
    "hanasu": "話します",
    "taberu": "食べます",
    "miru": "見ます",
    "iku": "行きます",
    "kuru": "来ます",
    "hataraku": "働きます",
    "benkyou": "勉強します",

    "suki": "好きです",
    "tokui": "得意です",

    "ryouri": "料理",
    "undou": "運動",
    "tsuri": "釣り",

    "unten": "運転",
    "pasokon": "パソコン",

    "shigoto": "仕事",
    "koujou": "工場",

    "arigatou": "ありがとうございます",
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
# DETECT ROMAJI
# =====================================================

def is_romaji(text):

    text = text.lower().strip()

    if contains_japanese(text):

        return False

    pattern = re.fullmatch(

        r"[a-zA-Z\s\-]+",

        text
    )

    return bool(pattern)


# =====================================================
# ROMAJI CONVERTER
# =====================================================

def romaji_to_japanese(text):

    words = text.lower().split()

    result = []

    for word in words:

        if word in ROMAJI_MAP:

            result.append(
                ROMAJI_MAP[word]
            )

        else:

            result.append(word)

    return " ".join(result)


# =====================================================
# FORMAL JAPANESE NORMALIZER
# =====================================================

def normalize_japanese(text):

    replacements = {

        # =========================================
        # dictionary -> polite
        # =========================================

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

        # =========================================
        # casual -> polite
        # =========================================

        "したい": "したいです",
        "好き": "好きです",
        "得意": "得意です",
        "趣味": "趣味です",

        # =========================================
        # remove rough/plain forms
        # =========================================

        "している": "しています",
        "してる": "しています",
        "やっている": "やっています",
        "やってる": "やっています",

        # =========================================
        # natural cv wording
        # =========================================

        "ことができます": "できます",
        "することができます": "できます",

        # =========================================
        # too casual words
        # =========================================

        "とても": "大変",
        "いっぱい": "多く",

        # =========================================
        # cleaner japanese
        # =========================================

        "ですです": "です",
        "ますます": "ます",

        # =========================================
        # N4 STANDARD KANJI
        # =========================================

        "にほん": "日本",
        "にほんご": "日本語",
        "がっこう": "学校",
        "かいしゃ": "会社",
        "せんせい": "先生",
        "べんきょう": "勉強",
        "しごと": "仕事",
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    return text


# =====================================================
# ENSURE POLITE ENDING
# =====================================================

def ensure_polite(text):

    polite_endings = (

        "です",
        "ます",
        "ません",
        "ました",
        "できます",
        "しております",
        "あります",
    )

    if text.endswith(polite_endings):

        return text

    # =============================================
    # SHORT NOUN
    # =============================================

    if (
        "。" not in text
        and len(text) <= 20
    ):

        return text + "です"

    return text


# =====================================================
# CLEAN EXTRA SPACES
# =====================================================

def clean_text(text):

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()


# =====================================================
# MAIN FUNCTION
# =====================================================

def translate_to_japanese(text):

    if not text:

        return ""

    text = clean_text(text)

    lower_text = text.lower()

    # =================================================
    # CUSTOM TRANSLATION
    # =================================================

    if lower_text in CUSTOM_TRANSLATIONS:

        return CUSTOM_TRANSLATIONS[
            lower_text
        ]

    try:

        # =================================================
        # CASE 1
        # USER INPUT JAPANESE
        # =================================================

        if contains_japanese(text):

            result = normalize_japanese(
                text
            )

            result = ensure_polite(
                result
            )

            return result

        # =================================================
        # CASE 2
        # USER INPUT ROMAJI
        # =================================================

        if is_romaji(text):

            result = romaji_to_japanese(
                text
            )

            result = normalize_japanese(
                result
            )

            result = ensure_polite(
                result
            )

            return result

        # =================================================
        # CASE 3
        # INDONESIAN -> JAPANESE
        # =================================================

        result = GoogleTranslator(

            source="id",

            target="ja"

        ).translate(text)

        result = normalize_japanese(
            result
        )

        result = ensure_polite(
            result
        )

        return result

    except:

        return text