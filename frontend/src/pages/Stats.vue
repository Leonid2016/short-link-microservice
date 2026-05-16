<script setup>
import { onMounted, ref } from "vue";
import { fetchStats } from "../api";

const props = defineProps({ code: String });

const data = ref(null);
const error = ref("");
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  error.value = "";
  try {
    data.value = await fetchStats(props.code);
  } catch (e) {
    error.value = e?.message || "Ошибка";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Аналитика</h1>
      <p class="text-sm text-slate-500">Код: <span class="font-medium text-slate-900">{{ code }}</span></p>
    </div>

    <p v-if="error" class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
      {{ error }}
    </p>

    <div v-if="loading" class="text-sm text-slate-500">Загрузка…</div>

    <div v-else-if="data" class="grid gap-4 lg:grid-cols-3">
      <div class="rounded-2xl border bg-white p-5 shadow-sm lg:col-span-2">
        <div class="text-sm text-slate-500">Оригинальная ссылка</div>
        <a class="mt-1 block break-words font-medium text-slate-900 underline" :href="data.link.original_url" target="_blank">
          {{ data.link.original_url }}
        </a>

        <div class="mt-4 grid gap-3 sm:grid-cols-3">
          <div class="rounded-xl border bg-slate-50 p-4">
            <div class="text-xs text-slate-500">Всего кликов</div>
            <div class="mt-1 text-2xl font-semibold">{{ data.total_clicks }}</div>
          </div>

          <div class="rounded-xl border bg-slate-50 p-4">
            <div class="text-xs text-slate-500">Статус</div>
            <div class="mt-2">
              <span
                class="inline-flex items-center rounded-full px-2 py-0.5 text-xs border"
                :class="data.link.is_active ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-slate-200 bg-slate-50 text-slate-600'"
              >
                {{ data.link.is_active ? "Активна" : "Выключена" }}
              </span>
            </div>
          </div>

          <div class="rounded-xl border bg-slate-50 p-4">
            <div class="text-xs text-slate-500">Expires</div>
            <div class="mt-1 text-sm text-slate-700">
              {{ data.link.expires_at || "—" }}
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-2xl border bg-white p-5 shadow-sm">
        <div class="text-sm font-semibold">Топ источников</div>
        <p class="text-xs text-slate-500">Откуда приходят переходы</p>

        <div class="mt-3 space-y-2">
          <div
            v-for="r in data.top_referers"
            :key="r.referer"
            class="flex items-center justify-between rounded-xl border bg-slate-50 px-3 py-2 text-sm"
          >
            <div class="truncate pr-3">{{ r.referer }}</div>
            <div class="font-medium">{{ r.count }}</div>
          </div>

          <div v-if="data.top_referers.length === 0" class="text-sm text-slate-500">
            Пока нет данных.
          </div>
        </div>
      </div>

      <div class="rounded-2xl border bg-white p-5 shadow-sm lg:col-span-2">
        <div class="text-sm font-semibold">Клики по дням (14 дней)</div>
        <p class="text-xs text-slate-500">Агрегация по датам</p>

        <div class="mt-3 overflow-hidden rounded-xl border">
          <table class="min-w-full text-sm">
            <thead class="bg-slate-50 text-slate-600">
              <tr>
                <th class="px-4 py-2 text-left font-medium">День</th>
                <th class="px-4 py-2 text-left font-medium">Клики</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in data.by_day" :key="r.day" class="border-t">
                <td class="px-4 py-2 text-slate-700">{{ r.day }}</td>
                <td class="px-4 py-2 font-medium">{{ r.count }}</td>
              </tr>
              <tr v-if="data.by_day.length === 0" class="border-t">
                <td class="px-4 py-3 text-slate-500" colspan="2">Нет данных за последние дни.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="rounded-2xl border bg-white p-5 shadow-sm">
        <div class="text-sm font-semibold">Последние клики</div>
        <p class="text-xs text-slate-500">Последние 20 событий</p>

        <div class="mt-3 space-y-2 max-h-[360px] overflow-auto pr-1">
          <div
            v-for="c in data.last_clicks"
            :key="c.clicked_at + c.referer"
            class="rounded-xl border bg-slate-50 p-3"
          >
            <div class="text-xs text-slate-500">{{ c.clicked_at }}</div>
            <div class="mt-1 text-sm text-slate-700 truncate">{{ c.referer }}</div>
          </div>

          <div v-if="data.last_clicks.length === 0" class="text-sm text-slate-500">
            Пока кликов нет.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
