import "./style.css";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { loadAuth } from "./authStore";

loadAuth();

createApp(App).use(router).mount("#app");
