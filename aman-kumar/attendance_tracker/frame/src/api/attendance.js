import { fetchWithAuth } from '../api/token';

const API_BASE = 'http://localhost:9123/v1/user';

export async function getAttendanceSummary(emp_id = '', summary_date = '') {
  let url = `${API_BASE}/attendance/daily-summary`;
  const params = [];
  if (emp_id) params.push(`emp_id=${encodeURIComponent(emp_id)}`);
  if (summary_date) params.push(`summary_date=${encodeURIComponent(summary_date)}`);
  if (params.length > 0) url += '?' + params.join('&');
  const res = await fetchWithAuth(url);
  if (!res.ok) throw new Error('Failed to fetch attendance summary');
  return res.json();
}

export async function punchAttendance(action) {
  const res = await fetchWithAuth(`${API_BASE}/attendance/punch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  });
  if (!res.ok) throw new Error('Failed to punch attendance');
  return res.json();
}

export async function getAttendanceByEmpId(emp_id, date_str) {
  let url = `${API_BASE}/attendance/by-emp_id?emp_id=${encodeURIComponent(emp_id)}&date_str=${encodeURIComponent(date_str)}`;
  const res = await fetchWithAuth(url);
  if (!res.ok) throw new Error('Failed to fetch attendance by emp_id');
  return res.json();
}

export async function getAttendanceByUsername(username, date_str) {
  let url = `${API_BASE}/attendance/by-username?username=${encodeURIComponent(username)}&date_str=${encodeURIComponent(date_str)}`;
  const res = await fetchWithAuth(url);
  if (!res.ok) throw new Error('Failed to fetch attendance by username');
  return res.json();
}

export async function deleteAttendanceByEmpId(emp_id) {
  const url = `${API_BASE}/attendance/delete?emp_id=${encodeURIComponent(emp_id)}`;
  const res = await fetchWithAuth(url, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete attendance');
  return res.json();
}

export async function deleteAttendanceByEmpIdAndDay(emp_id, date_str) {
  const url = `${API_BASE}/attendance/delete_by_day?emp_id=${encodeURIComponent(emp_id)}&date_str=${encodeURIComponent(date_str)}`;
  const res = await fetchWithAuth(url, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete attendance by day');
  return res.json();
}
