import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import Links from "./pages/Links.vue";
import Stats from "./pages/Stats.vue";
import Login from "./pages/Login.vue";
import AdminUsers from "./pages/AdminUsers.vue";
import Register from "./pages/Register.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", component: Login },
    { path: "/", component: Home },
    { path: "/links", component: Links },
    { path: "/stats/:code", component: Stats, props: true },
    { path: "/admin/users", component: AdminUsers },
	{ path: "/register", component: Register },

  ],
});

router.beforeEach((to) => {
  console.log("?? ROUTE TO:", to.path);

  const token = localStorage.getItem("token");
  const publicPaths = ["/", "/login", "/register"];

  if (!token && !publicPaths.includes(to.path)) {
    console.log("? REDIRECT TO /login");
    return "/login";
  }

  const role = localStorage.getItem("role");
  if (to.path.startsWith("/admin") && role !== "admin") {
    return "/links";
  }

  console.log("? ALLOWED");
});


export default router;
