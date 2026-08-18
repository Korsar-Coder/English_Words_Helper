import "./homepage.css";
import axios from "axios";

document.addEventListener("DOMContentLoaded", () => {
  const logout_button = document.querySelector("#logout-button");
  const words_container = document.querySelector("#words-container");
  const start_quiz_button = document.querySelector("#start-quiz-button");
  const snowgrave_button = document.querySelector("#snowgrave-button");
  const addCardTrigger = document.createElement("div");
  const base_url = "http://localhost:8000/api";

  if (!words_container) {
    console.log(window.another_theme);
    console.error("Element #words-container not found!");
    return;
  }

  const cards = words_container.querySelectorAll(".word-card");
  const welcome_text = document.querySelector("#welcome-text");
  const snowContainer = document.querySelector(".snow-container");

  const default_colors = {
    start_quiz_button_background_color: "rgb(255, 240, 153)",
    welcome_text_color: "yellow",
    card_background_color: "beige",
  };

  var incorrect_input = document.querySelector(".incorrect-input");
  let wordsList;
  window.another_theme = false;

  snowgrave_button.addEventListener("click", () => {
    if (!window.another_theme) {
      change_theme();
      window.another_theme = true;
    } else {
      change_theme_back();
      window.another_theme = false;
    }
  });

  function start_snow_falling() {
    snowContainer.style.opacity = 0.8;
    snowContainer.style.visibility = "visible";
    const snowflakesCount = 50; // количество снежинок

    for (let i = 0; i < snowflakesCount; i++) {
      const snowflake = document.createElement("div");
      snowflake.classList.add("snowflake");

      // Случайный размер, положение и скорость падения
      const size = Math.random() * 6 + 2 + "px";
      snowflake.style.width = size;
      snowflake.style.height = size;
      snowflake.style.left = Math.random() * 100 + "vw";
      snowflake.style.animationDuration = Math.random() * 3 + 2 + "s"; // от 2 до 5 секунд
      snowflake.style.animationDelay = Math.random() * 5 + "s";

      snowContainer.appendChild(snowflake);
    }
  }

  function change_theme() {
    if (start_quiz_button) {
      start_quiz_button.style.backgroundColor = "#ff5e5e";
    }
    if (welcome_text) {
      welcome_text.style.color = "#1c9bca";
    }
    cards.forEach((card) => {
      card.style.backgroundColor = "#68bbd9";
      const translation = card.querySelector(".word-translation");
      if (translation) {
        translation.style.color = "black";
      }
    });
    start_snow_falling();
  }

  function change_theme_back() {
    if (start_quiz_button) {
      start_quiz_button.style.backgroundColor =
        default_colors.start_quiz_button_background_color;
    }
    if (welcome_text) {
      welcome_text.style.color = default_colors.welcome_text_color;
    }
    cards.forEach((card) => {
      card.style.backgroundColor = default_colors.card_background_color;
      const translation = card.querySelector(".word-translation");
      if (translation) {
        translation.style.color = "black";
      }
    });
    snowContainer.style.opacity = 0;
    setTimeout(() => {
      snowContainer.style.visibility = "hidden";
    }, 500);
    snowContainer.replaceChildren();
  }

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

  function build_word(word, is_origin_english = true) {
    const card = document.createElement("div");
    card.classList.add("word-card");
    card.dataset.id = word.id;
    if (!is_origin_english) {
      card.innerHTML = `
    <button class="delete-word-btn" title="Удалить слово">&times;</button>
    <div class="word-origin">${word.translation || "Идёт перевод..."}</div>
    <div class="word-translation">${word.origin}</div>
  `;
      card.dataset.english_word = word.translation;
    } else {
      card.innerHTML = `
    <button class="delete-word-btn" title="Удалить слово">&times;</button>
    <div class="word-origin">${word.origin}</div>
    <div class="word-translation">${word.translation || "Идёт перевод..."}</div>
  `;
      card.dataset.english_word = word.origin;
    }
    const deleteBtn = card.querySelector(".delete-word-btn");
    deleteBtn.addEventListener("click", async (event) => {
      event.stopPropagation(); // Предотвращаем срабатывание клика по самой карточке, если оно у вас настроено
      console.log("Процесс удаления...");
      const nextSibling = card.nextSibling;
      try {
        // Отправляем DELETE-запрос на бэкенд, передавая id слова в URL
        var removed_card = card;
        card.remove();
        const deleteResponse = await axios.delete(
          `${base_url}/delete_word_by_id/${card.dataset.id}`,
          {
            withCredentials: true,
          },
        );

        if (deleteResponse.data.status === "success") {
          // Если сервер успешно удалил из БД, плавно удаляем карточку со страницы
          console.log(`Слово с id ${card.dataset.id} успешно удалено`);
          wordsList = wordsList.filter(
            (w) => String(w.Users_word?.id) !== String(card.dataset.id),
          );
          // if (card.dataset.english_word == forbidden_word) {
          //   snowContainer.style.visibility = "hidden";
          //   location.reload();
          // }
        }
      } catch (error) {
        console.error("Ошибка при удалении слова:", error);
        //Если не получилось удалить слово, возвращаем его
        if (nextSibling) {
          words_container.insertBefore(card, nextSibling);
        } else {
          words_container.appendChild(card);
        }
        alert(error.response?.data?.detail || "Не удалось удалить слово.");
      }
    });
    return card;
  }

  async function get_words() {
    try {
      let response = await axios.get(base_url + "/get_user_words", {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });

      wordsList = response.data;
      console.log("Слова пользователя: ", wordsList);
      words_container.innerHTML = "";

      for (let wordData of wordsList) {
        const word = wordData["Users_word"];

        const card = build_word(word);

        // Добавляем готовую карточку в общий контейнер
        words_container.appendChild(card);
      }

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
            origin: originText,
            translation: translationText,
            is_origin_english: is_origin_english,
          };

          const word_template = {
            origin: originText,
            translation: translationText,
            word_id: -1,
          };

          const new_card = build_word(word_template, is_origin_english);
          words_container.replaceChild(new_card, formCard);
          words_container.appendChild(addCardTrigger);
          try {
            const addResponse = await axios.post(
              base_url + "/add_word",
              wordData,
              {
                withCredentials: true,
              },
            );
            const result = addResponse.data;
            new_card.dataset.id = result["word_id"];
            if (is_origin_english) {
              new_card.dataset.english_word = originText;
              const translationDiv =
                new_card.querySelector(".word-translation");
              if (translationDiv) {
                translationDiv.textContent = result["translation"];
              }
            } else {
              const translationDiv = new_card.querySelector(".word-origin");
              new_card.dataset.english_word = result["translation"];
              if (translationDiv) {
                translationDiv.textContent = result["translation"];
              }
            }
            wordsList.push({
              Users_word: {
                id: result["word_id"],
                origin: originText,
                translation: result["translation"],
              },
            });
            console.log("Слово добавлено:", result);
          } catch (error) {
            console.error("Ошибка добавления слова:", error);
            new_card.remove();
            guardDashboard();
            location.reload();
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
    if (wordsList.length < 4) {
      incorrect_input.style.visibility = "visible";
      console.log("Мало слов");
      setTimeout(() => {
        incorrect_input.style.visibility = "hidden";
      }, 3000);
      return;
    }

    window.location.href = "/quiz.html";
  });

  guardDashboard();
  get_words();
});
