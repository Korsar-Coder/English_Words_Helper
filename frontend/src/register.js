import "./auth-register.css";
import axios from "axios";

const base_url = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", () => {
  const formElement = document.querySelector("#register-form");

  if (!formElement) return;

  const inputs = document.querySelectorAll("#register-form input");

  inputs[0].focus();

  inputs.forEach((input, index) => {
    input.addEventListener("keydown", (e) => {
      let targetInput = null;

      // Логика переключения
      switch (e.key) {
        case "ArrowRight":
        case "ArrowDown":
          // Переход вперед (если есть следующий, иначе к первому)
          targetInput = inputs[index + 1] || inputs[0];
          break;
        case "ArrowLeft":
        case "ArrowUp":
          // Переход назад (если есть предыдущий, иначе к последнему)
          targetInput = inputs[index - 1] || inputs[inputs.length - 1];
          break;
      }

      // Если нашли нужный инпут, переводим фокус
      if (targetInput) {
        e.preventDefault(); // Отменяем стандартное перемещение курсора/скролл
        targetInput.focus();
        targetInput.select(); // Выделяем текст в поле (по желанию)
      }
    });
  });

  formElement.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(formElement);
    const map_data = Object.fromEntries(formData);

    if (map_data["password"] != map_data["password-repeat"]) {
      alert("Пароль не совпадает!");
      return;
    }

    const request_data = {
      name: map_data["username"],
      raw_password: map_data["password"],
    };
    console.log("Данные для отправки: ", request_data);
    const backend_url = base_url + "/register";
    try {
      const response = await axios.post(backend_url, request_data, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      });
      console.log(response.data);
      window.location.href = "/homepage.html";
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

async function checkAuthOnRegisterSkin() {
  try {
    await axios.get(base_url + "/check-auth", {
      withCredentials: true,
    });
    // Если запрос успешный (кука есть) -> отправляем на главную
    window.location.href = "/homepage.html";
  } catch (error) {
    // Если ошибка (куки нет) -> ничего не делаем, пусть пользователь заполняет форму
    console.log("Пользователь не авторизован, показываем форму");
    console.log(error);
  }
}

checkAuthOnRegisterSkin();
