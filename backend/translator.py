import httpx


async def translate(text: str, from_lang: str = "en", to_lang="ru") -> str:
    if not text:
        return
    url = "http://translator:5000/translate"

    # Формат параметров для LibreTranslate API
    payload = {"q": text, "source": from_lang, "target": to_lang, "format": "text"}

    async with httpx.AsyncClient() as client:
        try:
            # Отправляем неблокирующий POST-запрос
            response = await client.post(url, data=payload, timeout=5.0)

            if response.status_code == 200:
                # Сервис возвращает JSON, забираем оттуда переведенную строку
                return response.json().get("translatedText", text)
            else:
                print(f"[⚠️ WARNING] Ошибка переводчика: {response.status_code}.")
                return text
        except Exception as e:
            print(f"[❌ ERROR] Не удалось связаться с микросервисом перевода: {e}")
            return text
