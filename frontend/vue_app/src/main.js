import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import router from "./router";
import fetchUtil from "./plugins/fetchUtil"

createApp(App).use(router).use(store).use(fetchUtil).mount("#app");
