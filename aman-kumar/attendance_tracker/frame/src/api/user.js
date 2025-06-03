import { fetchWithAuth } from '../api/token';

const API_BASE = 'http://localhost:9123/v1/user';

export async function getCurrentUser() {
  const res = await fetchWithAuth(`${API_BASE}/current-user`);
  if (!res.ok) throw new Error('Failed to fetch user info');
  return res.json();
}

export async function getAllUsers() {
  const res = await fetchWithAuth(`${API_BASE}/all`);
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
}

export async function getUserByUsername(username) {
  const res = await fetchWithAuth(`${API_BASE}/users/${username}`);
  if (!res.ok) throw new Error('Failed to fetch user');
  return res.json();
}

export async function updateUser(username, data) {
  const res = await fetchWithAuth(`${API_BASE}/users/${username}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error('Failed to update user');
  return res.json();
}

export async function deleteUser(username) {
  const res = await fetchWithAuth(`${API_BASE}/users/${username}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to delete user');
  return res.json();
}

export async function changePassword(currentPassword, newPassword, confirmPassword) {
  const res = await fetchWithAuth(`${API_BASE}/change-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword, confirm_password: confirmPassword })
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to change password');
  }
  return res.json();
}

export async function getUserByEmpId(emp_id) {
  const res = await fetchWithAuth(`${API_BASE}/users/by-emp_id/${emp_id}`);
  if (!res.ok) throw new Error('Failed to fetch user by emp_id');
  return res.json();
}

// New API functions for forgot password flow

export async function forgotPassword(email) {
  const res = await fetch(`${API_BASE}/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to send forgot password email');
  }
  return res.json();
}

export async function resetPassword(token, newPassword) {
  const res = await fetch(`${API_BASE}/reset-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, new_password: newPassword })
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to reset password');
  }
  return res.json();
}
