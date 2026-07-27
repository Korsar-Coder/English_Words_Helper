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

      if (wordsList.length === 0) {
        words_container.innerHTML = no_words_html;
        return;
      }

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

          // Подтверждение удаления для пользователя (по желанию)
          if (
            !confirm(
              `Вы уверены, что хотите удалить слово "${word.origin}" с id ${word.id}?`,
            )
          )
            return;

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
