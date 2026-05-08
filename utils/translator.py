from deep_translator import GoogleTranslator

def translate_to_japanese(text):
    if not text:
        return ""

    try:
        result = GoogleTranslator(
            source='id',
            target='ja'
        ).translate(text)

        return result

    except:
        return text 