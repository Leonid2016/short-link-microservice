// frontend/src/authStore.js
import { reactive } from "vue";

export const auth = reactive({
  token: "",
  role: "",
  email: "",
});

export function loadAuth() {
  auth.token = localStorage.getItem("token") || "";
  auth.role = localStorage.getItem("role") || "";
  auth.email = localStorage.getItem("email") || "";
}

export function setAuth({ token, role, email }) {
  localStorage.setItem("token", token);
  localStorage.setItem("role", role);
  localStorage.setItem("email", email);

  auth.token = token;
  auth.role = role;
  auth.email = email;
}

export function clearAuth() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("email");

  auth.token = "";
  auth.role = "";
  auth.email = "";
}
