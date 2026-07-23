import "./auth-register.css";
import axios from "axios";

const base_url = "http://localhost:8000/api";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await axios.get(base_url + "/get_current_quiz_words", {
      withCredentials: true,
    });
    console.log(response.data);
  } catch (error) {
    console.log(error.message);
    window.location.href = "/auth.html";
  }
});
