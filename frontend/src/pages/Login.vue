<script setup>
import { ref } from "vue";
import { login } from "../api";
import { useRouter } from "vue-router";

const email = ref("admin@example.com");
const password = ref("123");
const error = ref("");
const loading = ref(false);
const router = useRouter();

function skip() {
  router.push("/");
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await login(email.value, password.value);
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
        <h1 class="text-xl font-semibold">Вход</h1>
        <p class="text-sm text-slate-500">Введите email и пароль</p>
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

        <button
          class="w-full rounded-xl bg-slate-900 px-4 py-2 text-white hover:bg-slate-800 disabled:opacity-60"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? "Входим..." : "Войти" }}
        </button>
		<button
			  class="w-full rounded-xl border bg-white px-4 py-2 text-slate-900 hover:bg-slate-50"
			  @click="skip"
			>
			  Пропустить авторизацию
			</button>	
        <p v-if="error" class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {{ error }}
        </p>

        <p class="text-sm text-slate-600">
          Нет аккаунта?
          <router-link class="text-slate-900 underline" to="/register">Регистрация</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
