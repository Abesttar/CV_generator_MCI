import re


# =====================================================
# SPECIAL WORDS
# =====================================================

SPECIAL_WORDS = {

    # islamic / umum
    "abdul": "アブドゥル",
    "abdur": "アブドゥル",
    "malik": "マリク",
    "muhammad": "ムハンマド",
    "mohammad": "モハマド",
    "mohamad": "モハマド",
    "muhamad": "ムハマド",
    "ahmad": "アフマド",
    "habibi": "ハビビ",

    # umum
    "elsa": "エルサ",
    "japasal": "ジャパサル",
    "jepasal": "ジェパサル",
}


# =====================================================
# KATAKANA MAP
# =====================================================

KATAKANA_MAP = {

    # =================================================
    # 4 LETTERS
    # =================================================

    "ltsu": "ッ",
    "xtsu": "ッ",

    # =================================================
    # 3 LETTERS
    # =================================================

    # kya
    "kya": "キャ",
    "kyu": "キュ",
    "kyo": "キョ",

    "gya": "ギャ",
    "gyu": "ギュ",
    "gyo": "ギョ",

    "sha": "シャ",
    "shu": "シュ",
    "sho": "ショ",

    "sya": "シャ",
    "syu": "シュ",
    "syo": "ショ",

    "cha": "チャ",
    "chu": "チュ",
    "cho": "チョ",

    "cya": "チャ",
    "cyu": "チュ",
    "cyo": "チョ",

    "tya": "チャ",
    "tyu": "チュ",
    "tyo": "チョ",

    "nya": "ニャ",
    "nyu": "ニュ",
    "nyo": "ニョ",

    "hya": "ヒャ",
    "hyu": "ヒュ",
    "hyo": "ヒョ",

    "mya": "ミャ",
    "myu": "ミュ",
    "myo": "ミョ",

    "rya": "リャ",
    "ryu": "リュ",
    "ryo": "リョ",

    "bya": "ビャ",
    "byu": "ビュ",
    "byo": "ビョ",

    "pya": "ピャ",
    "pyu": "ピュ",
    "pyo": "ピョ",

    # j
    "jya": "ジャ",
    "jyu": "ジュ",
    "jyo": "ジョ",

    "ja": "ジャ",
    "ju": "ジュ",
    "jo": "ジョ",

    # ts
    "tsa": "ツァ",
    "tsi": "ツィ",
    "tse": "ツェ",
    "tso": "ツォ",

    # d
    "dya": "ヂャ",
    "dyu": "ヂュ",
    "dyo": "ヂョ",

    # f
    "fa": "ファ",
    "fi": "フィ",
    "fe": "フェ",
    "fo": "フォ",

    # v
    "va": "ヴァ",
    "vi": "ヴィ",
    "vu": "ヴ",
    "ve": "ヴェ",
    "vo": "ヴォ",

    # kw
    "kwa": "クァ",
    "kwi": "クィ",
    "kwe": "クェ",
    "kwo": "クォ",

    # gw
    "gwa": "グァ",
    "gwi": "グィ",
    "gwe": "グェ",
    "gwo": "グォ",

    # modern
    "she": "シェ",
    "che": "チェ",
    "je": "ジェ",

    "thi": "ティ",
    "thu": "トゥ",

    "dhi": "ディ",
    "dhu": "ドゥ",

    "wha": "ウァ",
    "whi": "ウィ",
    "whe": "ウェ",
    "who": "ウォ",

    # indo natural
    "nya": "ニャ",
    "nga": "ンガ",
    "ngi": "ンギ",
    "ngu": "ング",
    "nge": "ンゲ",
    "ngo": "ンゴ",

    # =================================================
    # 2 LETTERS
    # =================================================

    "ts": "ツ",

    "shi": "シ",
    "chi": "チ",
    "tsu": "ツ",
    "fu": "フ",

    # k
    "ka": "カ",
    "ki": "キ",
    "ku": "ク",
    "ke": "ケ",
    "ko": "コ",

    # g
    "ga": "ガ",
    "gi": "ギ",
    "gu": "グ",
    "ge": "ゲ",
    "go": "ゴ",

    # s
    "sa": "サ",
    "si": "シ",
    "su": "ス",
    "se": "セ",
    "so": "ソ",

    # z
    "za": "ザ",
    "zi": "ジ",
    "zu": "ズ",
    "ze": "ゼ",
    "zo": "ゾ",

    # t
    "ta": "タ",
    "ti": "ティ",
    "tu": "トゥ",
    "te": "テ",
    "to": "ト",

    # d
    "da": "ダ",
    "di": "ディ",
    "du": "ドゥ",
    "de": "デ",
    "do": "ド",

    # n
    "na": "ナ",
    "ni": "ニ",
    "nu": "ヌ",
    "ne": "ネ",
    "no": "ノ",

    # h
    "ha": "ハ",
    "hi": "ヒ",
    "hu": "フ",
    "he": "ヘ",
    "ho": "ホ",

    # b
    "ba": "バ",
    "bi": "ビ",
    "bu": "ブ",
    "be": "ベ",
    "bo": "ボ",

    # p
    "pa": "パ",
    "pi": "ピ",
    "pu": "プ",
    "pe": "ペ",
    "po": "ポ",

    # m
    "ma": "マ",
    "mi": "ミ",
    "mu": "ム",
    "me": "メ",
    "mo": "モ",

    # y
    "ya": "ヤ",
    "yu": "ユ",
    "yo": "ヨ",

    # r
    "ra": "ラ",
    "ri": "リ",
    "ru": "ル",
    "re": "レ",
    "ro": "ロ",

    # w
    "wa": "ワ",
    "wo": "ヲ",

    # natural indo
    "ca": "チャ",
    "ci": "チ",
    "cu": "チュ",
    "ce": "チェ",
    "co": "コ",

    # l -> r japanese
    "la": "ラ",
    "li": "リ",
    "lu": "ル",
    "le": "レ",
    "lo": "ロ",
}


# =====================================================
# HELPERS
# =====================================================

VOWELS = ["a", "i", "u", "e", "o"]


def is_consonant(char):

    return (
        char.isalpha()
        and char not in VOWELS
    )


# =====================================================
# NORMALIZE INDONESIAN SOUND
# =====================================================

def normalize_word(word):

    replacements = {

        # islamic
        "kh": "h",
        "dh": "d",
        "th": "t",
        "dz": "z",

        # english
        "ph": "f",
        "ck": "k",
        "cq": "k",
        "qu": "ku",
        "q": "k",
        "x": "ks",

        # indonesia
        "sy": "sh",

        # natural
        "v": "vi",
    }

    for old, new in replacements.items():

        word = word.replace(old, new)

    return word


# =====================================================
# WORD TO KATAKANA
# =====================================================

def word_to_katakana(word):

    word = word.lower().strip()

    if not word:
        return ""

    # =========================================
    # SPECIAL WORDS
    # =========================================

    if word in SPECIAL_WORDS:
        return SPECIAL_WORDS[word]

    # =========================================
    # NORMALIZE
    # =========================================

    word = normalize_word(word)

    result = ""

    i = 0

    while i < len(word):

        # =====================================
        # DOUBLE CONSONANT
        # =====================================

        if (
            i + 1 < len(word)
            and word[i] == word[i + 1]
            and is_consonant(word[i])
            and word[i] != "n"
        ):

            result += "ッ"
            i += 1
            continue

        # =====================================
        # N -> ン
        # =====================================

        if word[i] == "n":

            if i == len(word) - 1:

                result += "ン"
                i += 1
                continue

            next_char = word[i + 1]

            if (
                next_char not in VOWELS
                and next_char != "y"
            ):

                result += "ン"
                i += 1
                continue

        matched = False

        # =====================================
        # MATCH 4,3,2,1
        # =====================================

        for length in [4, 3, 2, 1]:

            piece = word[i:i + length]

            if piece in KATAKANA_MAP:

                result += KATAKANA_MAP[piece]

                i += length

                matched = True

                break

        if matched:
            continue

        # =====================================
        # SINGLE CHAR FALLBACK
        # =====================================

        char = word[i]

        fallback_map = {

            "a": "ア",
            "i": "イ",
            "u": "ウ",
            "e": "エ",
            "o": "オ",

            "b": "ブ",
            "c": "ク",
            "d": "ド",
            "f": "フ",
            "g": "グ",
            "h": "ハ",
            "j": "ジ",
            "k": "ク",
            "l": "ル",
            "m": "ム",
            "p": "プ",
            "q": "ク",
            "r": "ル",
            "s": "ス",
            "t": "ト",
            "v": "ヴ",
            "w": "ウ",
            "x": "クス",
            "y": "イ",
            "z": "ズ",
        }

        result += fallback_map.get(char, "")

        i += 1

    # =========================================
    # CLEAN DUPLICATE VOWELS
    # =========================================

    result = result.replace("ウウ", "ウ")
    result = result.replace("イイ", "イ")

    return result


# =====================================================
# MAIN FUNCTION
# =====================================================

def latin_to_katakana(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    words = text.split()

    converted = []

    for word in words:

        katakana = word_to_katakana(word)

        if katakana:

            converted.append(katakana)

    return "・".join(converted)


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    names = [

        "suci oktaviani",
        "risyad ahmad",
        "oktovus richardo",
        "samuel prambanan",
        "cahya insani",
        "angga purnama",
        "acep farhan",
        "muhammad rizky",
        "abdul malik",
        "fadhlan ramadhan",
        "syahrul gunawan",
        "novita sari",
        "dewi lestari",
        "yusuf hamdan",
        "andika putra",
    ]

    for name in names:

        print(
            name,
            "->",
            latin_to_katakana(name)
        )