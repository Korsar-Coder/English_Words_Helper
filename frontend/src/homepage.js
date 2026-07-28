import "./homepage.css";
import axios from "axios";

// Запускаем в самом начале файла src/dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const logout_button = document.querySelector("#logout-button");
  const words_container = document.querySelector("#words-container");
  const start_quiz_button = document.querySelector("#start-quiz-button");
  const base_url = "http://localhost:8000/api";
  const no_words_html =
    '<p style="font-size: 50px; color: beige; font-family: Playfair Display">Ваш словарь пока пуст!</p>';

  async function guardDashboard() {
    try {
      await axios.get(base_url + "/check-auth", {
        withCredentials: true,
      });
      console.log("Добро пожаловать на главную страницу!");
      // Здесь инициализируйте остальной код главной страницы
    } catch (error) {
      console.log("Ошибка Куки");
      // Если сервер ответил ошибкой (куки нет/протухла) -> выкидываем на авторизацию
      window.location.href = "/auth.html";
    }
  }

  async function get_words() {
    try {
      let response = await axios.get(base_url + "/get_user_words", {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });

      const wordsList = response.data;
      console.log("Слова пользователя: ", wordsList);
      words_container.innerHTML = "";

      wordsList.forEach((word) => {
        word = word["Users_word"];
        const card = document.createElement("div");
        card.classList.add("word-card");
        card.innerHTML = `
    <button class="delete-word-btn" title="Удалить слово">&times;</button>
    <div class="word-origin">${word.origin}</div>
    <div class="word-translation">${word.translation}</div>
  `;
        const deleteBtn = card.querySelector(".delete-word-btn");
        deleteBtn.addEventListener("click", async (event) => {
          event.stopPropagation(); // Предотвращаем срабатывание клика по самой карточке, если оно у вас настроено

          try {
            // Отправляем DELETE-запрос на бэкенд, передавая id слова в URL
            const deleteResponse = await axios.delete(
              `${base_url}/delete_word_by_id/${word.id}`,
              {
                withCredentials: true,
              },
            );

            if (deleteResponse.data.status === "success") {
              // Если сервер успешно удалил из БД, плавно удаляем карточку со страницы
              card.remove();
              console.log(`Слово с id ${word.id} успешно удалено`);

              // Если после удаления карточек не осталось, выводим заглушку
              if (words_container.children.length === 0) {
                words_container.innerHTML =
                  "<p style='font-size: 24px; color: white;'>Ваш словарь теперь пуст!</p>";
              }
            }
          } catch (error) {
            console.error("Ошибка при удалении слова:", error);
            alert(error.response?.data?.detail || "Не удалось удалить слово.");
          }
        });

        // Добавляем готовую карточку в общий контейнер
        words_container.appendChild(card);
      });
      const addCardTrigger = document.createElement("div");
      addCardTrigger.classList.add("add-word-trigger-card");
      addCardTrigger.innerHTML = "+";
      addCardTrigger.title = "Добавить новое слово";
      addCardTrigger.addEventListener("click", () => {
        // Получаем структуру формы из HTML-шаблона <template>
        const template = document.querySelector("#add-word-template");
        const formCard = template.content
          .cloneNode(true)
          .querySelector(".add-word-form-card");

        // Временно заменяем кнопку-плюс на карточку с инпутами
        words_container.replaceChild(formCard, addCardTrigger);

        // Находим элементы управления внутри появившейся формы
        const saveBtn = formCard.querySelector("#save-word-btn");
        const cancelBtn = formCard.querySelector("#cancel-word-btn");
        const inputOrigin = formCard.querySelector("#new-origin");
        const inputTranslation = formCard.querySelector("#new-translation");

        inputOrigin.focus(); // Сразу ставим фокус на первое поле

        // Кнопка ОТМЕНА: просто возвращает кнопку-плюс на место
        cancelBtn.addEventListener("click", () => {
          words_container.replaceChild(addCardTrigger, formCard);
        });

        guardDashboard();

        // Кнопка СОХРАНИТЬ: отправка на бэкенд
        saveBtn.addEventListener("click", async () => {
          const originText = inputOrigin.value.trim();
          const translationText = inputTranslation.value.trim();

          if (originText.length < 2) {
            alert("Слово должно быть не короче 2 символов!");
            return;
          }

          //Проверяем, ввел ли пользователь слово на английском или русском
          let is_origin_english = true;
          let first_letter = originText.toLowerCase()[0];
          if ("а" <= first_letter && first_letter <= "я") {
            is_origin_english = false;
          }
          const wordData = {
            user_id: 0,
            origin: originText,
            translation: translationText,
            is_origin_english: is_origin_english,
          };

          try {
            const addResponse = await axios.post(
              base_url + "/add_word",
              wordData,
              {
                withCredentials: true,
              },
            );

            console.log("Слово добавлено:", addResponse.data);

            get_words();
          } catch (error) {
            console.error("Ошибка добавления слова:", error);
            alert("Не удалось сохранить слово.");
          }
        });
      });

      // Добавляем созданный плюс в самый конец контейнера
      words_container.appendChild(addCardTrigger);
    } catch (error) {
      console.log(error);
    }
    guardDashboard();
  }

  logout_button.addEventListener("click", async (event) => {
    event.preventDefault();
    let response = await axios.post(
      base_url + "/logout",
      {},
      {
        withCredentials: true,
      },
    );
    window.location.href = "/auth.html";
  });

  start_quiz_button.addEventListener("click", async (event) => {
    event.preventDefault();
    if (words_container.innerHTML == no_words_html) {
      alert("У вас нет слов!");
      return;
    }

    window.location.href = "/quiz.html";
  });

  guardDashboard();
  get_words();
});
