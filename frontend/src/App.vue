<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { logout } from "./api";
import { auth } from "./authStore";

const router = useRouter();
const role = computed(() => auth.role);
const email = computed(() => auth.email);

function doLogout() {
  logout();
  router.push("/login");
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <header class="border-b bg-white/80 backdrop-blur">
      <div class="mx-auto max-w-6xl px-4 py-4 flex items-center gap-4">
        <div class="flex items-center gap-3">
          <div class="h-10 w-10 rounded-2xl bg-slate-900 text-white grid place-items-center font-semibold">
            LS
          </div>
          <div>
            <div class="font-semibold leading-tight">LinkShort</div>
            <div class="text-xs text-slate-500 leading-tight">Flask • Postgres • Vue</div>
          </div>
        </div>

        <nav class="ml-6 flex items-center gap-3 text-sm">
          <router-link class="px-3 py-2 rounded-xl hover:bg-slate-100" to="/">Главная</router-link>
          <router-link class="px-3 py-2 rounded-xl hover:bg-slate-100" to="/links">Ссылки</router-link>
          <router-link
            v-if="role === 'admin'"
            class="px-3 py-2 rounded-xl hover:bg-slate-100"
            to="/admin/users"
          >
            Пользователи
          </router-link>
        </nav>

        <div class="ml-auto flex items-center gap-3">
          <span v-if="email" class="text-sm text-slate-600">
            {{ email }}
            <span v-if="role" class="ml-2 inline-flex items-center rounded-full border px-2 py-0.5 text-xs">
              {{ role }}
            </span>
          </span>

          <button
            class="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800"
            @click="doLogout"
          >
            Выйти
          </button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8">
      <router-view />
    </main>
  </div>
</template>
