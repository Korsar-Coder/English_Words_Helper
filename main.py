import requests
import asyncio
import googletrans
from time import sleep
import random as rand
import streamlit as st

# path = "https://api.dictionaryapi.dev/api/v2/entries/en/<word>"

translator = googletrans.Translator()
state = st.session_state

class Word_Info:
    origin: str
    
    grade: int

    def __init__(self, grade = 5, **kwargs):
        self.grade = grade
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    async def write_translation(self):
        self.translation = await translator.translate(self.origin,"ru", "en")

if "words" not in state and "set_words" not in state:
    state.words = []
    state.set_words = set()

if "tasks" not in state: state.tasks = []

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

async def main():
    container = st.container()
    new_word = container.text_input("Слово/Выражение для запоминания")
    add_button = container.button("Добавить")
    check_button = container.button("Посмотреть перевод")
    if add_button:
        if not new_word in state.set_words:
            state.words.append(Word_Info(grade=5,origin = new_word))
            state.tasks.append(state.words[len(state.words) - 1].write_translation())
            state.set_words.add(new_word)
    st.write(state.words)
    if check_button:
        await asyncio.gather(*state.tasks)
        state.tasks = []
        pairs = {}
        for word in state.words:
            if hasattr(word, 'translation'):
                pairs[word.origin] = word.translation.text
            else: pairs[word.origin] = "Переводится..."  
        st.write(pairs)          

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
    asyncio.run(main())