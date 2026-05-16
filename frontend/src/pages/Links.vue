<script setup>
import { onMounted, ref, computed } from "vue";
import { fetchLinks, setActive } from "../api";

const items = ref([]);
const error = ref("");
const loading = ref(false);

const role = computed(() => localStorage.getItem("role") || "user");

// Админ-фильтры
const q = ref("");
const user = ref("");
const from = ref("");
const to = ref("");

function toIsoOrEmpty(dtLocal) {
  if (!dtLocal) return "";
  return new Date(dtLocal).toISOString();
}

function buildQuery() {
  if (role.value !== "admin") return "";
  const p = new URLSearchParams();
  if (q.value.trim()) p.set("q", q.value.trim());
  if (user.value.trim()) p.set("user", user.value.trim());
  if (from.value) p.set("from", toIsoOrEmpty(from.value));
  if (to.value) p.set("to", toIsoOrEmpty(to.value));
  return p.toString();
}

function formatDate(val) {
  if (!val) return "—";
  // если приходит ISO — отформатируем локально
  const d = new Date(val);
  if (Number.isNaN(d.getTime())) return String(val);
  return d.toLocaleString();
}

function daysLeft(expiresAt) {
  if (!expiresAt) return null;
  const d = new Date(expiresAt);
  if (Number.isNaN(d.getTime())) return null;
  const ms = d.getTime() - Date.now();
  return Math.ceil(ms / (1000 * 60 * 60 * 24));
}

async function load() {
  loading.value = true;
  error.value = "";
  try {
    const query = buildQuery();
    items.value = await fetchLinks(query);
  } catch (e) {
    error.value = e?.message || "Ошибка";
  } finally {
    loading.value = false;
  }
}

async function toggle(it) {
  try {
    await setActive(it.code, !it.is_active);
    await load();
  } catch (e) {
    error.value = e?.message || "Ошибка";
  }
}

function clearFilters() {
  q.value = "";
  user.value = "";
  from.value = "";
  to.value = "";
  load();
}

async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {}
}

onMounted(load);
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-end justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold">Ссылки</h1>
        <p class="text-sm text-slate-500">
          {{ role === "admin" ? "Админ: все ссылки + фильтры." : "Пользователь: только ваши ссылки." }}
        </p>
      </div>

      <button class="rounded-xl border bg-white px-3 py-2 text-sm hover:bg-slate-50" @click="load">
        Обновить
      </button>
    </div>

    <!-- Фильтры админа -->
    <div v-if="role === 'admin'" class="rounded-2xl border bg-white p-4 shadow-sm">
      <div class="grid gap-3 md:grid-cols-4">
        <div>
          <div class="text-xs text-slate-500">Поиск (код/оригинал/название)</div>
          <input
            v-model="q"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
            placeholder="abc123 или example.com"
          />
        </div>

        <div>
          <div class="text-xs text-slate-500">Пользователь (email)</div>
          <input
            v-model="user"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
            placeholder="user@mail.com"
          />
        </div>

        <div>
          <div class="text-xs text-slate-500">Дата: с</div>
          <input
            v-model="from"
            type="datetime-local"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
          />
        </div>

        <div>
          <div class="text-xs text-slate-500">Дата: по</div>
          <input
            v-model="to"
            type="datetime-local"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
          />
        </div>
      </div>

      <div class="mt-3 flex gap-2">
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800" @click="load">
          Применить
        </button>
        <button class="rounded-xl border bg-white px-4 py-2 text-sm hover:bg-slate-50" @click="clearFilters">
          Сбросить
        </button>
      </div>
    </div>

    <p v-if="error" class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
      {{ error }}
    </p>

    <div v-if="loading" class="text-sm text-slate-500">Загрузка…</div>

    <!-- Карточки (без горизонтального скролла) -->
    <div v-else class="grid gap-3">
      <div
        v-for="it in items"
        :key="it.id"
        class="rounded-2xl border bg-white p-4 shadow-sm"
      >
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="min-w-0">
            <!-- TITLE -->
            <div class="text-sm font-semibold text-slate-900 truncate">
              {{ it.title || "Без названия" }}
            </div>

            <!-- CODE + STATUS -->
            <div class="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-600">
              <router-link class="underline" :to="`/stats/${it.code}`">Код: {{ it.code }}</router-link>

              <span
                class="inline-flex items-center rounded-full px-2 py-0.5 text-xs border"
                :class="it.is_active ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-slate-200 bg-slate-50 text-slate-600'"
              >
                {{ it.is_active ? "Активна" : "Выключена" }}
              </span>

              <span v-if="role==='admin' && it.user_email" class="inline-flex items-center rounded-full border px-2 py-0.5">
                {{ it.user_email }}
              </span>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <a
              class="rounded-xl border bg-white px-3 py-1.5 text-xs hover:bg-slate-50"
              :href="it.short_url"
              target="_blank"
            >
              Открыть
            </a>

            <button
              class="rounded-xl border bg-white px-3 py-1.5 text-xs hover:bg-slate-50"
              @click="copy(it.short_url)"
            >
              Copy
            </button>

            <button
              v-if="role==='admin'"
              class="rounded-xl bg-slate-900 px-3 py-1.5 text-xs text-white hover:bg-slate-800"
              @click="toggle(it)"
            >
              {{ it.is_active ? "Выключить" : "Включить" }}
            </button>
          </div>
        </div>

        <!-- LINKS -->
        <div class="mt-3 grid gap-2 md:grid-cols-2">
          <div class="rounded-xl border bg-slate-50 p-3">
            <div class="text-xs text-slate-500">Короткая</div>
            <a class="mt-1 block break-words text-sm font-medium text-slate-900 underline" :href="it.short_url" target="_blank">
              {{ it.short_url }}
            </a>
          </div>

          <div class="rounded-xl border bg-slate-50 p-3">
            <div class="text-xs text-slate-500">Оригинал</div>
            <a class="mt-1 block break-words text-sm text-slate-700 underline" :href="it.original_url" target="_blank">
              {{ it.original_url }}
            </a>
          </div>
        </div>

        <!-- META -->
        <div class="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          <div class="text-xs text-slate-600">
            <span class="text-slate-500">Создана:</span>
            <span class="ml-1">{{ formatDate(it.created_at) }}</span>
          </div>

          <div class="text-xs text-slate-600">
            <span class="text-slate-500">Истекает:</span>
            <span class="ml-1">{{ formatDate(it.expires_at) }}</span>

            <template v-if="it.expires_at">
              <span
                v-if="daysLeft(it.expires_at) !== null"
                class="ml-2 inline-flex items-center rounded-full border px-2 py-0.5"
                :class="daysLeft(it.expires_at) <= 0
                  ? 'border-red-200 bg-red-50 text-red-700'
                  : daysLeft(it.expires_at) <= 7
                    ? 'border-amber-200 bg-amber-50 text-amber-800'
                    : 'border-slate-200 bg-white text-slate-600'"
              >
                {{
                  daysLeft(it.expires_at) <= 0
                    ? "истекла"
                    : "осталось " + daysLeft(it.expires_at) + " дн."
                }}
              </span>
            </template>
          </div>

          <div class="text-xs text-slate-600">
            <span class="text-slate-500">Статистика:</span>
            <router-link class="ml-1 underline" :to="`/stats/${it.code}`">открыть</router-link>
          </div>
        </div>
      </div>

      <div v-if="items.length === 0" class="rounded-2xl border bg-white p-6 text-sm text-slate-500">
        Ничего не найдено.
      </div>
    </div>
  </div>
</template>
