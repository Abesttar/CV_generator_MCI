import re


KATAKANA_MAP = {
    "a": "ア",
    "i": "イ",
    "u": "ウ",
    "e": "エ",
    "o": "オ",

    "ka": "カ",
    "ki": "キ",
    "ku": "ク",
    "ke": "ケ",
    "ko": "コ",

    "sa": "サ",
    "shi": "シ",
    "su": "ス",
    "se": "セ",
    "so": "ソ",

    "ta": "タ",
    "chi": "チ",
    "tsu": "ツ",
    "te": "テ",
    "to": "ト",

    "na": "ナ",
    "ni": "ニ",
    "nu": "ヌ",
    "ne": "ネ",
    "no": "ノ",

    "ha": "ハ",
    "hi": "ヒ",
    "fu": "フ",
    "he": "ヘ",
    "ho": "ホ",

    "ma": "マ",
    "mi": "ミ",
    "mu": "ム",
    "me": "メ",
    "mo": "モ",

    "ya": "ヤ",
    "yu": "ユ",
    "yo": "ヨ",

    "ra": "ラ",
    "ri": "リ",
    "ru": "ル",
    "re": "レ",
    "ro": "ロ",

    "wa": "ワ",
    "wo": "ヲ",
    "n": "ン",

    "ga": "ガ",
    "gi": "ギ",
    "gu": "グ",
    "ge": "ゲ",
    "go": "ゴ",

    "za": "ザ",
    "ji": "ジ",
    "zu": "ズ",
    "ze": "ゼ",
    "zo": "ゾ",

    "da": "ダ",
    "de": "デ",
    "do": "ド",

    "ba": "バ",
    "bi": "ビ",
    "bu": "ブ",
    "be": "ベ",
    "bo": "ボ",

    "pa": "パ",
    "pi": "ピ",
    "pu": "プ",
    "pe": "ペ",
    "po": "ポ",

    "kya": "キャ",
    "kyu": "キュ",
    "kyo": "キョ",

    "sha": "シャ",
    "shu": "シュ",
    "sho": "ショ",

    "cha": "チャ",
    "chu": "チュ",
    "cho": "チョ",

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

    "gya": "ギャ",
    "gyu": "ギュ",
    "gyo": "ギョ",

    "bya": "ビャ",
    "byu": "ビュ",
    "byo": "ビョ",

    "pya": "ピャ",
    "pyu": "ピュ",
    "pyo": "ピョ",

    "fa": "ファ",
    "fi": "フィ",
    "fe": "フェ",
    "fo": "フォ",

    "va": "ヴァ",
    "vi": "ヴィ",
    "vu": "ヴ",
    "ve": "ヴェ",
    "vo": "ヴォ",

    "sy": "シャ",
    "kh": "ク",
    "dz": "ズ",
    "dh": "ド",
    "th": "ト",
}


def word_to_katakana(word):

    word = word.lower()

    result = ""
    i = 0

    while i < len(word):

        matched = False

        for length in [3, 2, 1]:

            piece = word[i:i+length]

            if piece in KATAKANA_MAP:

                result += KATAKANA_MAP[piece]
                i += length
                matched = True
                break

        if not matched:
            i += 1

    return result


def latin_to_katakana(text):

    if not text:
        return ""

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    words = text.split()

    converted = []

    for word in words:
        converted.append(
            word_to_katakana(word)
        )

    return "・".join(converted)