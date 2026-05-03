/**
 * AuraStyle API Service
 * IT22590794 - Rajapaksha P D P P
 *
 * Complete API client for all Flask backend endpoints.
 * Uses plain fetch — no external dependencies.
 */

// ─────────────────────────────────────────────
// BASE URL  (set VITE_API_URL in frontend/.env)
// ─────────────────────────────────────────────

const BASE_URL =
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) ||
  'http://localhost:5000';

// ─────────────────────────────────────────────
// LOW-LEVEL HELPERS
// ─────────────────────────────────────────────

async function doFetch(input, init) {
  const res  = await fetch(input, init);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ?? `HTTP ${res.status}`);
  return data;
}

function jsonPost(endpoint, body) {
  return doFetch(`${BASE_URL}${endpoint}`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
  });
}

function formPost(endpoint, form) {
  return doFetch(`${BASE_URL}${endpoint}`, { method: 'POST', body: form });
}

// ─────────────────────────────────────────────
// WARDROBE CRUD
// ─────────────────────────────────────────────

function getWardrobe(params = {}) {
  const q = new URLSearchParams(params).toString();
  return doFetch(`${BASE_URL}/api/wardrobe${q ? '?' + q : ''}`);
}

function getItem(id) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}`);
}

function addItem(item) {
  return doFetch(`${BASE_URL}/api/wardrobe`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(item),
  });
}

function updateItem(id, updates) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}`, {
    method:  'PUT',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(updates),
  });
}

function deleteItem(id) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}`, { method: 'DELETE' });
}

function toggleFavourite(id) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}/favourite`, { method: 'PATCH' });
}

function toggleAvailability(id, isAvailable) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}/availability`, {
    method:  'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ isAvailable }),
  });
}

function incrementUsage(id) {
  return doFetch(`${BASE_URL}/api/wardrobe/${id}/use`, { method: 'PATCH' });
}

// ─────────────────────────────────────────────
// ANALYTICS
// ─────────────────────────────────────────────

function getAnalytics() {
  return doFetch(`${BASE_URL}/api/analytics`);
}

function getActivity(limit = 20) {
  return doFetch(`${BASE_URL}/api/activity?limit=${limit}`);
}

// ─────────────────────────────────────────────
// MODEL ENDPOINTS
// ─────────────────────────────────────────────

/** Health check */
function checkHealth() {
  return doFetch(`${BASE_URL}/api/health`);
}

/** Model 1 — classify accessory image */
function classifyAccessory(imageFile) {
  const form = new FormData();
  form.append('image', imageFile);
  return formPost('/api/classify-accessory', form);
}

/** Model 2 — extract dress attributes */
function extractDressAttributes(imageFile) {
  const form = new FormData();
  form.append('image', imageFile);
  return formPost('/api/extract-dress-attributes', form);
}

/** Model 3 — fuse dress + metadata */
function fuseFeatures(params) {
  return jsonPost('/api/fuse-features', params);
}

/** Model 4 — DQN recommendations */
function getRecommendations(params) {
  return jsonPost('/api/recommend', params);
}

/** Full pipeline — one call for Discover page */
function runFullPipeline(params) {
  const form = new FormData();
  form.append('image',    params.imageFile);
  form.append('occasion', params.occasion);
  form.append('religion', params.religion ?? 'None');
  form.append('gender',   params.gender);
  form.append('budget',   String(params.budget ?? 5000));
  form.append('wardrobe', JSON.stringify(params.wardrobe ?? []));
  return formPost('/api/full-pipeline', form);
}

/** Explain a specific recommendation */
function explainItem(params) {
  return jsonPost('/api/explain', params);
}

/** Explainable AI chat */
function chat(message, context) {
  return jsonPost('/api/chat', { message, context });
}

// ─────────────────────────────────────────────
// UNIFIED api OBJECT  (imported by WardrobeContext & other components)
// ─────────────────────────────────────────────
export const api = {
  // Wardrobe CRUD
  getWardrobe,
  getItem,
  addItem,
  updateItem,
  deleteItem,
  toggleFavourite,
  toggleAvailability,
  incrementUsage,

  // Analytics & activity
  getAnalytics,
  getActivity,

  // Models
  checkHealth,
  classifyAccessory,
  extractDressAttributes,
  fuseFeatures,
  getRecommendations,
  recommend: runFullPipeline,   // alias used by Discover page
  explainItem,
  chat,
};

export default api;