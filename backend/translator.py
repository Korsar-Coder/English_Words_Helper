import googletrans

translator = googletrans.Translator()


async def translate(text: str, from_lang: str = "en", to_lang="ru") -> str:
    if not text.strip():
        return

    translation = await translator.translate(text=text, src=from_lang, dest=to_lang)
    return translation.text
