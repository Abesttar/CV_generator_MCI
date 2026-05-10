import re


SPECIAL_WORDS = {

    "abdul": "アブドゥル",
    "malik": "マリク",
    "muhammad": "ムハンマド",
    "mohammad": "モハマド",
    "ahmad": "アフマド",
    "habibi": "ハビビ",
    "elsa": "エルサ",
    "japasal": "ジャパサル",
    "jepasal": "ジェパサル",
}


KATAKANA_MAP = {

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

    "tsu": "ツ",
    "shi": "シ",
    "chi": "チ",
    "fu": "フ",

    "ja": "ジャ",
    "ju": "ジュ",
    "jo": "ジョ",

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
    "su": "ス",
    "se": "セ",
    "so": "ソ",

    "ta": "タ",
    "te": "テ",
    "to": "ト",

    "na": "ナ",
    "ni": "ニ",
    "nu": "ヌ",
    "ne": "ネ",
    "no": "ノ",

    "ha": "ハ",
    "hi": "ヒ",
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
}


def word_to_katakana(word):

    word = word.lower()

    if word in SPECIAL_WORDS:
        return SPECIAL_WORDS[word]

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

            char = word[i]

            if char == "l":
                result += "ル"

            elif char == "v":
                result += "ヴ"

            elif char == "c":
                result += "ク"

            elif char == "q":
                result += "ク"

            elif char == "x":
                result += "クス"

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