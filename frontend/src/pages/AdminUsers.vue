<script setup>
import { onMounted, ref } from "vue";
import { fetchUsers } from "../api";

const q = ref("");
const items = ref([]);
const error = ref("");
const loading = ref(false);

async function load() {
  loading.value = true;
  error.value = "";
  try {
    items.value = await fetchUsers(q.value.trim());
  } catch (e) {
    error.value = e?.message || "Ошибка";
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Пользователи</h1>
      <p class="text-sm text-slate-500">Доступно только администратору.</p>
    </div>

    <div class="rounded-2xl border bg-white p-4 shadow-sm">
      <div class="flex gap-2">
        <input
          v-model="q"
          class="w-full rounded-xl border px-3 py-2 outline-none focus:ring-2 focus:ring-slate-200"
          placeholder="поиск по email"
        />
        <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800" @click="load">
          Найти
        </button>
      </div>
    </div>

    <p v-if="error" class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
      {{ error }}
    </p>

    <div v-if="loading" class="text-sm text-slate-500">Загрузка…</div>

    <div v-else class="rounded-2xl border bg-white shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-slate-50 text-slate-600">
            <tr>
              <th class="px-4 py-3 text-left font-medium">Email</th>
              <th class="px-4 py-3 text-left font-medium">Role</th>
              <th class="px-4 py-3 text-left font-medium">Created</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in items" :key="u.id" class="border-t">
              <td class="px-4 py-3">{{ u.email }}</td>
              <td class="px-4 py-3">
                <span
                  class="inline-flex items-center rounded-full border px-2 py-0.5 text-xs"
                  :class="u.role==='admin' ? 'border-slate-900 bg-slate-900 text-white' : 'border-slate-200 bg-slate-50 text-slate-700'"
                >
                  {{ u.role }}
                </span>
              </td>
              <td class="px-4 py-3 text-slate-600 whitespace-nowrap">{{ u.created_at }}</td>
            </tr>

            <tr v-if="items.length === 0" class="border-t">
              <td class="px-4 py-4 text-slate-500" colspan="3">Пользователи не найдены.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
