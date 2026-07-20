import "./homepage.css";
import axios from "axios";

// Запускаем в самом начале файла src/dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const get_words_button = document.querySelector("#get-words-button");
  const base_url = "http://localhost:8000/api";

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
  guardDashboard();

  get_words_button.addEventListener("click", async (event) => {
    event.preventDefault();
    try {
      let response = await axios.get(base_url + "/get_user_words", {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });
      console.log(response);
    } catch (error) {
      console.log(error);
    }
    guardDashboard();
  });
});
