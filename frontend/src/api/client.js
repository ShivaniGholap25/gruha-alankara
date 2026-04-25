const BASE_URL = '';

export async function apiFetch(path, options = {}) {
  const defaultOptions = {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (options.body instanceof FormData) {
    delete defaultOptions.headers['Content-Type'];
  }

  try {
    const response = await fetch(BASE_URL + path, defaultOptions);
    const data = await response.json().catch(() => ({}));
    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    console.error('API Error:', error);
    return { ok: false, status: 0, data: { error: 'Network error' } };
  }
}

export const api = {
  get: (path) => apiFetch(path, { method: 'GET' }),
  post: (path, body) => apiFetch(path, { 
    method: 'POST', 
    body: body instanceof FormData ? body : JSON.stringify(body)
  }),
  delete: (path) => apiFetch(path, { method: 'DELETE' }),
};
