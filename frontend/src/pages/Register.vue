<script setup>
import { ref } from "vue";
import { register } from "../api";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const password2 = ref("");
const error = ref("");
const loading = ref(false);
const router = useRouter();

async function submit() {
  error.value = "";
  if (!email.value || !password.value) {
    error.value = "Введите email и пароль";
    return;
  }
  if (password.value !== password2.value) {
    error.value = "Пароли не совпадают";
    return;
  }

  loading.value = true;
  try {
    await register(email.value, password.value);
    router.push("/links");
  } catch (e) {
    error.value = e.message || "Ошибка";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="grid place-items-center">
    <div class="w-full max-w-md rounded-2xl border bg-white p-6 shadow-sm">
      <div class="mb-4">
        <h1 class="text-xl font-semibold">Регистрация</h1>
        <p class="text-sm text-slate-500">Создайте аккаунт пользователя</p>
      </div>

      <div class="space-y-3">
        <div>
          <label class="text-sm text-slate-600">Email</label>
          <input v-model="email" class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-300"
                 placeholder="you@example.com" />
        </div>

        <div>
          <label class="text-sm text-slate-600">Пароль</label>
          <input v-model="password" type="password"
                 class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-300"
                 placeholder="••••••••" />
        </div>

        <div>
          <label class="text-sm text-slate-600">Повтор пароля</label>
          <input v-model="password2" type="password"
                 class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-300"
                 placeholder="••••••••" />
        </div>

        <button
          class="w-full rounded-xl bg-slate-900 px-4 py-2 text-white hover:bg-slate-800 disabled:opacity-60"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? "Создаём..." : "Зарегистрироваться" }}
        </button>

        <p v-if="error" class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {{ error }}
        </p>

        <p class="text-sm text-slate-600">
          Уже есть аккаунт?
          <router-link class="text-slate-900 underline" to="/login">Войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
