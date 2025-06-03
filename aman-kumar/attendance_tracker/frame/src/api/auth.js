const API_BASE = 'https://attendance-tracker-project.onrender.com/v1/user';

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (res.ok && data.access_token) {
    localStorage.setItem('access_token', data.access_token);
    if (data.refresh_token) localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  } else {
    throw new Error(data.detail || 'Login failed');
  }
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

export function getAccessToken() {
  return localStorage.getItem('access_token');
}

// Use fetchWithAuth for authenticated API calls if needed in the future
