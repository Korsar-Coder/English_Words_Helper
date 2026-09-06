import httpx
import urllib.parse


async def translate(text: str, from_lang: str = "en", to_lang="ru") -> str:
    if not text.strip():
        return

    # Переводим пробелы и знаки в формат url
    encoded_text = urllib.parse.quote(text)
    url = f"https://googleapis.com{from_lang}&tl={to_lang}&dt=t&q={encoded_text}"
    # Формат параметров для LibreTranslate API
    payload = {"q": text, "source": from_lang, "target": to_lang, "format": "text"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload, timeout=5.0)

            if response.status_code == 200:
                return response.json().get("translatedText", text)
            else:
                print(f"[⚠️ WARNING] Ошибка переводчика: {response.status_code}.")
                return text
        except Exception as e:
            print(f"[❌ ERROR] Не удалось связаться с микросервисом перевода: {e}")
            return text
