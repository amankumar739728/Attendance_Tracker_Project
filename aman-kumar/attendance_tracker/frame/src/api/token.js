const API_BASE = 'http://localhost:9123/v1/user';

export async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) throw new Error('No refresh token');
  const res = await fetch(`${API_BASE}/refresh-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  const data = await res.json();
  if (!res.ok || !data.access_token) throw new Error('Failed to refresh token');
  localStorage.setItem('access_token', data.access_token);
  if (data.refresh_token) localStorage.setItem('refresh_token', data.refresh_token);
  return data;
}

export async function fetchWithAuth(url, options = {}) {
  let token = localStorage.getItem('access_token');
  options.headers = options.headers || {};
  options.headers['Authorization'] = `Bearer ${token}`;
  let response = await fetch(url, options);
  if (response.status === 401) {
    try {
      await refreshAccessToken();
      token = localStorage.getItem('access_token');
      options.headers['Authorization'] = `Bearer ${token}`;
      response = await fetch(url, options);
    } catch (err) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
      throw err;
    }
  }
  return response;
}

// Add periodic background refresh for access token
export function startPeriodicTokenRefresh(intervalMinutes = 15) {
  // Clear any previous interval
  if (window._tokenRefreshInterval) clearInterval(window._tokenRefreshInterval);
  window._tokenRefreshInterval = setInterval(() => {
    refreshAccessToken().catch(() => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    });
  }, intervalMinutes * 60 * 1000);
}
