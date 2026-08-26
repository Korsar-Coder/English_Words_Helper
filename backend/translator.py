from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError


def translate(text: str, from_lang: str = "en", to_lang="ru") -> str:
    text = text.strip()
    if not text:
        return text
    try:
        return GoogleTranslator(source=from_lang, target=to_lang).translate(text)
    except (RequestError, TranslationNotFound, Exception) as e:
        print(f"Google translate error: {e}. Trying MyMemory")
        try:
            return MyMemoryTranslator(source=from_lang, target=to_lang).translate(text)
        except Exception as fallback_error:
            print("Translators are fallen")
            return text
