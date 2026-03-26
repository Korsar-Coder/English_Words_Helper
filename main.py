import requests
import translate
import asyncio
import googletrans
from time import sleep
import random

path = "https://api.dictionaryapi.dev/api/v2/entries/en/<word>"

translator = googletrans.Translator()

class Word:
    origin: str
    translation: str
    grade: int

    def __init__(self, grade = 5, **kwargs):
        self.grade = grade
        for key, value in kwargs.items():
            setattr(self, key, value)


words: list[Word] = []

async def add_word(word: str):
    global words
    translation = await translator.translate(word, dest="ru", src="en")
    words.append(Word(origin = word, translation= translation.text))  
    
async def main():
    tasks = []
    while True:
        answer = input("Слово для запоминания: ").strip()
        if answer: 
            tasks.append(asyncio.create_task(add_word(answer)))
        else: break
    await asyncio.gather(*tasks)
    words_amount = len(words)
    if words_amount == 1:
        print("Вы ввели всего одно слово!")
        return
    print("Слова:")
    print([word.__dict__ for word in words])
    print("-" * 15 + "\nЗадаем вопросы!")
    while True:
        rand_index = random.randint(0, words_amount - 1)
        checking_word = words[rand_index] 
        other_words = words[:rand_index] + words[rand_index + 1:]
        
        fun_number = random.randint(1, 3)
        if fun_number == 1:
            fake_words = 

if __name__ == "__main__":
    asyncio.run(main())