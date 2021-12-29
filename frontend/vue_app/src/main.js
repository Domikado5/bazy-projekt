import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import router from "./router";

createApp(App).use(router).use(store).mount("#app");
