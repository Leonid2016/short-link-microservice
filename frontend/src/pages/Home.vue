<script setup>
import { ref } from "vue";
import { createLink } from "../api";
import { computed } from "vue";
const original_url = ref("");
const title = ref("");
const custom_alias = ref("");
const expires_at = ref(""); // datetime-local

const loading = ref(false);
const error = ref("");
const result = ref(null);
const isGuest = computed(() => !localStorage.getItem("token"));

function toIsoOrUndefined(dtLocal) {
  if (!dtLocal) return undefined;
  return new Date(dtLocal).toISOString();
}

async function submit() {
  error.value = "";
  result.value = null;

  if (!original_url.value.trim()) {
    error.value = "Введите исходную ссылку";
    return;
  }

  loading.value = true;
  try {
    const expiresIso = toIsoOrUndefined(expires_at.value);
    result.value = await createLink({
      original_url: original_url.value.trim(),
      title: title.value.trim() || undefined,
      custom_alias: custom_alias.value.trim() || undefined,
      expires_at: expiresIso,
    });

    // слегка очистим
    // original_url.value = "";
    // title.value = "";
    // custom_alias.value = "";
    // expires_at.value = "";
  } catch (e) {
    error.value = e?.message || "Ошибка";
  } finally {
    loading.value = false;
  }
}

async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // игнор
  }
}
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-2">
    <section class="rounded-2xl border bg-white p-6 shadow-sm">
      <div class="mb-4">
        <h1 class="text-xl font-semibold">Сократить ссылку</h1>
        <p class="text-sm text-slate-500">
          Создавайте короткие ссылки, задавайте алиас и срок действия.
        </p>
      </div>

      <div class="space-y-4">
        <div>
          <label class="text-sm text-slate-600">Исходная ссылка</label>
          <input
            v-model="original_url"
            placeholder="https://example.com/very/long/url"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
          />
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="text-sm text-slate-600">Название</label>
            <input
              v-model="title"
              placeholder="Напр. YouTube"
              class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
            />
          </div>

          <div v-if="!isGuest">
            <label class="text-sm text-slate-600">Алиас (опционально)</label>
            <input
              v-model="custom_alias"
              placeholder="mylink"
              class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
            />
          </div>
        </div>

        <div v-if="!isGuest">
          <label class="text-sm text-slate-600">Истекает (опционально)</label>
          <input
            v-model="expires_at"
            type="datetime-local"
            class="mt-1 w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
          />
          <p class="mt-1 text-xs text-slate-500">
            Выбери дату/время через календарь. В БД сохраняется в UTC.
          </p>
        </div>
	    <p v-else class="text-xs text-slate-500">
		  Гостевой режим: алиас недоступен, срок действия = 30 дней.
		</p>		
        <button
          class="w-full rounded-xl bg-slate-900 px-4 py-2 text-white hover:bg-slate-800 disabled:opacity-60"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? "Создаём..." : "Сократить" }}
        </button>

        <p
          v-if="error"
          class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {{ error }}
        </p>
      </div>

    </section>

    <section class="rounded-2xl border bg-white p-6 shadow-sm">
      <div class="mb-4">
        <h2 class="text-lg font-semibold">Результат</h2>
        <p class="text-sm text-slate-500">После создания появится короткая ссылка.</p>
      </div>

      <div v-if="!result" class="text-sm text-slate-500">
        Пока пусто. Создай ссылку слева.
      </div>

      <div v-else class="space-y-3">
        <div class="rounded-xl border bg-slate-50 p-4">
          <div class="text-xs text-slate-500">Короткая ссылка</div>
          <div class="mt-1 flex items-center gap-2">
            <a class="font-medium text-slate-900 underline" :href="result.short_url" target="_blank">
              {{ result.short_url }}
            </a>
            <button
              class="rounded-lg border bg-white px-2 py-1 text-xs hover:bg-slate-50"
              @click="copy(result.short_url)"
            >
              Copy
            </button>
          </div>
        </div>

        <div class="rounded-xl border bg-slate-50 p-4">
          <div class="text-xs text-slate-500">Исходная</div>
          <div class="mt-1 break-words text-sm text-slate-800">
            {{ result.original_url || original_url }}
          </div>
        </div>

        <div class="text-xs text-slate-500">
          Подсказка: статистика будет в разделе “Ссылки” → клик по коду.
        </div>
      </div>
    </section>
  </div>
</template>
