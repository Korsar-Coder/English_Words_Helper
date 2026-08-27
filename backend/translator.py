from deep_translator import GoogleTranslator, MyMemoryTranslator, MicrosoftTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError


def translate(text: str, from_lang: str = "english", to_lang="russian") -> str:
    text = text.strip()
    if not text:
        return text
    try:
        return GoogleTranslator(source=from_lang, target=to_lang).translate(text)
    except (RequestError, Exception) as e:
        print(f"Google translate error: {e}. Trying MyMemory")
        try:
            return MyMemoryTranslator(source=from_lang, target=to_lang).translate(text)
        except Exception as fallback_error:
            print("Translators are fallen")
            return text
