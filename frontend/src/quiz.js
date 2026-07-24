import axios from "axios";

const base_url = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", async () => {
  let questions = [];
  let currentQuestionIndex = 0;
  let score = 0;

  const quizContainer = document.querySelector("#quiz-container");
  const resultContainer = document.querySelector("#result-container");
  const progressElement = document.querySelector("#progress");
  const wordElement = document.querySelector("#question-word");
  const choicesContainer = document.querySelector("#choices-container");
  const scoreText = document.querySelector("#score-text");

  // 1. Защита страницы (Проверка авторизации) и загрузка вопросов
  try {
    await axios.get(base_url + "/check-auth", { withCredentials: true });

    // Загружаем сгенерированные сервером вопросы
    const response = await axios.get(base_url + "/get_current_quiz_words", {
      withCredentials: true,
    });
    questions = response.data;

    // Запускаем первый вопрос
    showQuestion();
  } catch (error) {
    console.error(error);
    alert(
      error.response?.data?.detail ||
        "Ошибка загрузки теста. Возможно, у вас мало слов.",
    );
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
    resultContainer.style.display = "block";
    scoreText.textContent = `Правильных ответов: ${score} из ${questions.length}`;
  }
});
