import "./homepage.css";
import axios from "axios";

// Запускаем в самом начале файла src/dashboard.js
async function guardDashboard() {
  try {
    await axios.get("http://localhost:8000/api/check-auth", {
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
