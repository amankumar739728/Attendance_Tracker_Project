import { fetchWithAuth } from '../api/token';

const API_BASE = 'https://attendance-tracker-project.onrender.com/v1/user';

export async function sendMessage(message) {
  const res = await fetchWithAuth(`${API_BASE}/chatbot/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}

export async function getTodayAttendance() {
  const res = await fetchWithAuth(`${API_BASE}/attendance/daily-summary`);
  if (!res.ok) throw new Error('Failed to fetch today\'s attendance');
  return res.json();
}

export async function getAttendanceByDate(dateStr) {
  const res = await fetchWithAuth(`${API_BASE}/attendance/daily-summary?summary_date=${dateStr}`);
  if (!res.ok) throw new Error('Failed to fetch attendance for date');
  return res.json();
}
