<template>
  <!-- container — стандартный класс Bootstrap. Он центрирует контент и делает отступы по бокам -->
  <!-- py-5 добавляет крупные отступы сверху и снизу карточки -->
  <div class="container py-5">
    <div class="row justify-content-center">
      <!-- col-md-6 говорит: на экранах компьютеров форма займет половину ширины (6 из 12 колонок) -->
      <div class="col-12 col-md-6">
        <!-- card — компонент Bootstrap для создания блоков с белым фоном и границами -->
        <!-- shadow-sm добавляет легкую красивую тень -->
        <div class="card shadow-sm">
          <!-- Заголовок карточки -->
          <div class="card-header bg-primary text-white text-center py-3">
            <h3 class="card-title mb-0 h5">Добавление нового слова</h3>
          </div>

          <!-- Тело карточки, где лежат инпуты -->
          <div class="card-body p-4">
            <!-- Форма. @submit.prevent блокирует стандартную перезагрузку страницы браузером -->
            <!-- Вместо этого запустится наша функция handleAddWord -->
            <form @submit.prevent="handleAddWord">
              <!-- Блок ввода английского слова -->
              <div class="mb-3">
                <label for="englishWord" class="form-label fw-bold"
                  >Слово на английском *</label
                >
                <!-- v-model связывает этот инпут с переменной englishWord в секции <script> -->
                <!-- form-control — это главный класс Bootstrap, делающий инпут красивым -->
                <input
                  type="text"
                  id="englishWord"
                  v-model.trim="englishWord"
                  class="form-control form-control-lg"
                  placeholder="Например: apple"
                  required
                />
              </div>

              <!-- Блок ввода перевода (необязательный) -->
              <div class="mb-4">
                <label for="translation" class="form-label fw-bold"
                  >Перевод (необязательно)</label
                >
                <input
                  type="text"
                  id="translation"
                  v-model.trim="translation"
                  class="form-control"
                  placeholder="Оставьте пустым для автоперевода"
                />
                <!-- text-muted делает текст мелким и серым (подсказка) -->
                <div class="form-text text-muted">
                  Если оставить поле пустым, слово будет переведено
                  автоматичски.
                </div>
              </div>

              <!-- Кнопка отправки -->
              <!-- btn-success делает её зеленой, w-100 растягивает на всю ширину карточки -->
              <button type="submit" class="btn btn-success btn-lg w-100">
                Добавить в словарь ✨
              </button>
            </form>

            <!-- Блок для вывода сообщений об успехе или ошибке -->
            <!-- v-if проверяет: если в переменной statusMessage есть текст, то этот блок покажется -->
            <div
              v-if="statusMessage"
              class="alert mt-4 text-center"
              :class="alertClass"
            >
              {{ statusMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// Создаем реактивные переменные через ref().
// Когда пользователь пишет текст в инпутах, значения этих переменных меняются автоматически.
const englishWord = ref("");
const translation = ref("");
const statusMessage = ref("");
const alertClass = ref("alert-info"); // Класс Bootstrap для цвета уведомления (синий, зеленый, красный)

// Функция, которая срабатывает при нажатии на кнопку отправки формы
const handleAddWord = async () => {
  // 1. Формируем объект с данными, который мы отправим на FastAPI
  const requestData = {
    word: englishWord.value,
    // Если пользователь ничего не ввел, отправляем null (или пустую строку),
    // чтобы бэкенд понял: нужно включить автоперевод
    translation: translation.value || null,
  };

  statusMessage.value = "Отправка данных на сервер...";
  alertClass.value = "alert-warning"; // Желтый цвет (загрузка)

  try {
    // 2. Здесь будет твой реальный запрос к FastAPI через axios
    // Пример: const response = await axios.post('http://localhost:8000/words', requestData)

    // Имитируем успешный ответ от сервера для наглядности:
    console.log("Данные успешно отправлены на бэкенд:", requestData);

    // Меняем статус на успешный (зеленый блок alert-success)
    alertClass.value = "alert-success";
    statusMessage.value = `Слово "${englishWord.value}" успешно добавлено!`;

    // 3. Очищаем поля формы после успешного добавления
    englishWord.value = "";
    translation.value = "";
  } catch (error) {
    // Если бэкенд упал или произошла ошибка сети — красим блок в красный (alert-danger)
    alertClass.value = "alert-danger";
    statusMessage.value = "Ошибка при добавлении слова. Проверьте подключение.";
    console.error(error);
  }
};
</script>

<style>
/* Благодаря Bootstrap, здесь нам вообще не нужно писать CSS код вручную! */
</style>
