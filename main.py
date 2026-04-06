import requests
import asyncio
import googletrans
from time import sleep
import random as rand
import streamlit as st

# path = "https://api.dictionaryapi.dev/api/v2/entries/en/<word>"

translator = googletrans.Translator()

class Word_Info:
    translation: str
    grade: int

    def __init__(self, grade = 5, **kwargs):
        self.grade = grade
        for key, value in kwargs.items():
            setattr(self, key, value)

if "words" not in st.session_state:
    st.session_state.words = {}

# async def add_word(word: str):
#     global words
#     translation = await translator.translate(word, dest="ru", src="en")
    # words.append(Word(origin = word, translation= translation.text))  
    
# def ask_words(checking_word: Word, other_words: list[Word]):
#     len_other = len(other_words) 
#     print(f"{checking_word} - ?:")
#     if len_other == 3:
#         fun_index = rand.randint(0,3)
#         sequnce = rand.sample(other_words, k = 3)
#         print(checking_word.origin + " - ?:")
#         for index, word in sequnce:
#             if index == fun_index:
#                 print("") 

# async def main():
def main():
    state = st.session_state
    container = st.container()
    new_word = container.text_input("Слово/Выражение для запоминания")
    add_button = container.button("Добавить")
    if add_button:
        state.words[new_word] = Word_Info()
    st.write(state.words)
    # tasks = []
    # while True:
    #     answer = input("Слово для запоминания: ").strip()
    #     if answer: 
    #         tasks.append(asyncio.create_task(add_word(answer)))
    #     else: break
    # await asyncio.gather(*tasks)
    # words_amount = len(words)
    # if words_amount == 1:
    #     print("Вы ввели всего одно слово!")
    #     return
    # print("Слова:")
    # print([word.__dict__ for word in words])
    # print("-" * 15 + "\nЗадаем вопросы!")
    # rand_index = -1
    # while True:
    #     if words_amount == 2:
    #         if rand_index == -1:
    #             rand_index = rand.randint(0,1)
    #             checking_word = words[rand_index]
    #             other_words = words[0] if rand_index == 1 else words[1]

    #     rand_index = rand.randint(0, words_amount - 1)
    #     checking_word = words[rand_index] 
    #     other_words = words[:rand_index] + words[rand_index + 1:]
    
    #     fun_number = rand.randint(1, 3)
    #     if fun_number == 1:
    #         fake_words = other_words

if __name__ == "__main__":
    # asyncio.run(main())
    main()