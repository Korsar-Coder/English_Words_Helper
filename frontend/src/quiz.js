import axios from "axios";

const base_url = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", async () => {
  let questions = [];
  let currentQuestionIndex = 0;
  let score = 0;

  console.log(window.another_theme);
  const quizContainer = document.querySelector("#quiz-container");
  const resultContainer = document.querySelector("#result-container");
  const progressElement = document.querySelector("#progress");
  const wordElement = document.querySelector("#question-word");
  const choicesContainer = document.querySelector("#choices-container");
  const scoreText = document.querySelector("#score-text");
  const snowContainer = document.querySelector(".snow-container");

  function start_snow_falling() {
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

  function change_start_theme() {
    quizContainer.style.background = "#6abfdf";
    resultContainer.style.background = "#1c9bca";
  }

  // 1. Защита страницы (Проверка авторизации) и загрузка вопросов
  try {
    await axios.get(base_url + "/check-auth", { withCredentials: true });

    // Загружаем сгенерированные сервером вопросы
    const response = await axios.get(base_url + "/get_current_quiz_words", {
      withCredentials: true,
    });
    questions = response.data["quiz_questions"];

    if (window.another_theme) {
      console.log("Другая тема..");
      change_start_theme();
      start_snow_falling();
    }
    // Запускаем первый вопрос
    showQuestion();
  } catch (error) {
    console.error(error);
    console.log("Ошибка");
    window.location.href = "/homepage.html";
  }

  // 2. Функция отображения текущего вопроса
  function showQuestion() {
    if (currentQuestionIndex >= questions.length) {
      showResults();
      return;
    }

    const currentQuestion = questions[currentQuestionIndex];

    // Обновляем прогресс и само слово
    progressElement.textContent = `Вопрос ${currentQuestionIndex + 1} из ${questions.length}`;
    wordElement.textContent = currentQuestion.english_word;

    // Очищаем старые кнопки вариантов
    choicesContainer.innerHTML = "";

    // Создаем 4 новые кнопки вариантов ответов
    currentQuestion.choices.forEach((choice) => {
      const button = document.createElement("button");
      button.textContent = choice;
      // Стилизация кнопок ответов

      button.classList.add("quiz-choice-btn");
      if (window.another_theme) {
        button.style.backgroundColor = "#ff9292";
      }
      // Обработка клика по ответу
      button.addEventListener("click", () =>
        handleAnswer(choice, currentQuestion.correct_answer),
      );
      choicesContainer.appendChild(button);
    });
  }

  // 3. Логика проверки ответа
  function handleAnswer(selectedChoice, correctChoice) {
    // Находим все кнопки вариантов в контейнере
    const buttons = choicesContainer.querySelectorAll(".quiz-choice-btn");

    buttons.forEach((btn) => {
      // Отключаем клики на время анимации, чтобы пользователь не нажал две кнопки сразу
      btn.style.pointerEvents = "none";

      if (btn.textContent === correctChoice) {
        btn.classList.add("correct"); // Подсвечиваем правильный зеленым
      }
      if (
        btn.textContent === selectedChoice &&
        selectedChoice !== correctChoice
      ) {
        btn.classList.add("incorrect"); // Если пользователь ошибся, подсвечиваем его выбор красным
      }
    });

    if (selectedChoice === correctChoice) {
      score++;
    }

    // Делаем небольшую паузу в 1 секунду (1000 мс), чтобы пользователь увидел результат,
    // и только потом переключаем вопрос
    setTimeout(() => {
      currentQuestionIndex++;
      showQuestion();
    }, 1000);
  }

  // 4. Отображение финального экрана результатов
  function showResults() {
    quizContainer.style.display = "none";
    if (window.another_theme) {
      const go_home_button = resultContainer.querySelector(
        "#go-home-button-quiz",
      );
      go_home_button.style.backgroundColor = "#ef7b7b";
    }
    resultContainer.style.display = "block";
    scoreText.textContent = `Правильных ответов: ${score} из ${questions.length}`;
  }
});
