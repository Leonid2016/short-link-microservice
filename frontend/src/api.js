// frontend/src/api.js

import { setAuth, clearAuth } from "./authStore";

const API = "/api";

/* =======================
   helpers
======================= */

function token() {
  return localStorage.getItem("token") || "";
}

async function req(path, options = {}) {
  const headers = { ...(options.headers || {}) };

  if (token()) {
    headers["Authorization"] = `Bearer ${token()}`;
  }

  return fetch(`${API}${path}`, {
    ...options,
    headers,
  });
}

async function parseJson(r) {
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

/* =======================
   auth
======================= */

export async function login(email, password) {
  const r = await req("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await parseJson(r);

  // реактивно обновляем auth
  setAuth({
    token: data.token,
    role: data.role,
    email: data.email,
  });

  return data;
}

export async function register(email, password) {
  const r = await req("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await parseJson(r);

  setAuth({
    token: data.token,
    role: data.role,
    email: data.email,
  });

  return data;
}

export function logout() {
  clearAuth();
}

/* =======================
   links
======================= */

export async function createLink(payload) {
  const r = await req("/links", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return parseJson(r);
}

export async function fetchLinks(query = "") {
  const r = await req(`/links${query ? `?${query}` : ""}`);
  const data = await parseJson(r);
  return data.items || [];
}

export async function setActive(code, is_active) {
  const r = await req(`/links/${encodeURIComponent(code)}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_active }),
  });

  return parseJson(r);
}

/* =======================
   analytics
======================= */

export async function fetchStats(code) {
  const r = await req(`/links/${encodeURIComponent(code)}/stats`);
  return parseJson(r);
}

/* =======================
   admin
======================= */

export async function fetchUsers(q = "") {
  const r = await req(`/admin/users${q ? `?q=${encodeURIComponent(q)}` : ""}`);
  const data = await parseJson(r);
  return data.items || [];
}
