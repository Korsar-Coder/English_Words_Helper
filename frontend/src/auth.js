import "./style.css";
import axios from "axios";

document.addEventListener("DOMContentLoaded", () => {
  const formElement = document.querySelector(".login-form");

  if (!formElement) return;

  formElement.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(formElement);
    const map_data = Object.fromEntries(formData);
    const request_data = {
      name: map_data["username"],
      raw_password: map_data["password"],
    };
    console.log("Данные для отправки: ", request_data);
    const backend_url = "http://localhost:8000/api/login";
    try {
      const response = await axios.post(backend_url, request_data, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      });
      console.log(response.data);
      window.location.href = "/dashboard.html";
    } catch (error) {
      console.error("Ошибка при отправке запроса:", error);

      if (error.response) {
        console.log("Статус ошибки:", error.response.status);
        console.log("Детали от сервера:", error.response.data);
        alert(
          `Ошибка авторизации: ${error.response.data.message || "Неверные данные"}`,
        );
      } else if (error.request) {
        alert("Сервер не отвечает. Проверьте интернет-соединение.");
      } else {
        alert("Произошла непредвиденная ошибка.");
      }
    }
  });
});

async function checkAuthOnLoginSkin() {
  try {
    await axios.get("http://localhost:8000/api/check-auth", {
      withCredentials: true,
    });
    // Если запрос успешный (кука есть) -> отправляем на главную
    window.location.href = "/dashboard.html";
  } catch (error) {
    // Если ошибка (куки нет) -> ничего не делаем, пусть пользователь заполняет форму
    console.log("Пользователь не авторизован, показываем форму");
    console.log(error);
  }
}

checkAuthOnLoginSkin();
