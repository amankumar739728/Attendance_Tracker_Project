// app.js - Handles API calls and UI logic

const API_BASE = "http://localhost:9123/v1/user"; // Change if your FastAPI runs elsewhere

// --- LOGIN ---
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (res.ok && data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                if (data.refresh_token) {
                    localStorage.setItem('refresh_token', data.refresh_token);
                }
                window.location.href = 'dashboard.html';
            } else {
                document.getElementById('loginError').innerText = data.detail || 'Login failed.';
            }
        } catch (err) {
            document.getElementById('loginError').innerText = 'Server error.';
        }
    });
}

// --- REGISTER ---
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const emp_id = document.getElementById('reg_emp_id').value;
        const username = document.getElementById('reg_username').value;
        const email = document.getElementById('reg_email').value;
        const password = document.getElementById('reg_password').value;
        const department = document.getElementById('reg_department').value;
        const sub_department = document.getElementById('reg_sub_department').value;
        // Remove is_admin from payload, always send as false
        try {
            const res = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emp_id, username, email, password, department, sub_department, is_admin: false })
            });
            const data = await res.json();
            if (res.ok) {
                window.location.href = 'login.html';
            } else {
                document.getElementById('registerError').innerText = data.detail || 'Registration failed.';
            }
        } catch (err) {
            document.getElementById('registerError').innerText = 'Server error.';
        }
    });
}

// Password show/hide toggle for registration
const toggleRegPassword = document.getElementById('toggleRegPassword');
if (toggleRegPassword) {
    const regPasswordInput = document.getElementById('reg_password');
    toggleRegPassword.addEventListener('click', () => {
        const isVisible = regPasswordInput.type === 'text';
        regPasswordInput.type = isVisible ? 'password' : 'text';
        toggleRegPassword.classList.toggle('fa-eye');
        toggleRegPassword.classList.toggle('fa-eye-slash');
    });
}

// --- TOKEN REFRESH LOGIC ---
function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return Promise.reject('No refresh token');
    return fetch(`${API_BASE}/refresh-token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed to refresh token');
        return res.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
        }
        // Only update refresh_token if backend returns a new one
        if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
        }
        return data;
    });
}

// --- AUTHENTICATED FETCH WITH AUTO REFRESH ---
async function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem('access_token');
    options.headers = options.headers || {};
    options.headers['Authorization'] = `Bearer ${token}`;

    let response = await fetch(url, options);

    if (response.status === 401) {
        // Try to refresh token
        try {
            await refreshAccessToken();
            // Retry original request with new token
            token = localStorage.getItem('access_token');
            options.headers['Authorization'] = `Bearer ${token}`;
            response = await fetch(url, options);
        } catch (err) {
            // Refresh failed, logout
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            alert('Session expired. Please log in again.');
            window.location.href = 'login.html';
            throw err;
        }
    }
    return response;
}

// --- DASHBOARD ---
if (window.location.pathname.endsWith('dashboard.html')) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
    }
    // Fetch user info
    fetchWithAuth(`${API_BASE}/current-user`)
    .then(res => res.json())
    .then(user => {
        document.getElementById('userInfo').innerHTML = `<b>User:</b> ${user.username} <br><b>Email:</b> ${user.email}`;
        // Show admin section if user is admin
        if (user.is_admin === true) {
            document.getElementById('adminSection').style.display = 'block';
            // Add filter UI for admin
            document.getElementById('adminSection').innerHTML = `
                <h3>Admin Controls</h3>
                <form id="filterForm" style="margin-bottom:16px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
                    <input type="text" id="filterEmpId" placeholder="Employee ID" style="padding:6px 8px;min-width:120px;">
                    <input type="date" id="filterDate" style="padding:6px 8px;">
                    <button type="submit" style="padding:6px 16px;">Apply Filter</button>
                    <button type="button" id="clearFilterBtn" style="padding:6px 16px;">Clear</button>
                </form>
            `;
        }
        // Function to fetch and render attendance logs (with optional filters)
        function fetchAndRenderAttendance(empId = '', summaryDate = '') {
            let url = `${API_BASE}/attendance/daily-summary`;
            const params = [];
            if (empId) params.push(`emp_id=${encodeURIComponent(empId)}`);
            if (summaryDate) params.push(`summary_date=${encodeURIComponent(summaryDate)}`);
            if (params.length > 0) url += '?' + params.join('&');
            fetchWithAuth(url)
            .then(res => res.json())
            .then(logs => {
                let html = '';
                // If admin and logs is an array, show all users (no filter)
                if (Array.isArray(logs) && logs.length > 0 && user.is_admin === true && !empId && !summaryDate) {
                    html += '<h3>All Users Attendance</h3>';
                    html += `<div style="overflow-x:auto;"><table style="min-width:700px;width:100%;border-collapse:collapse;word-break:break-word;">
                        <tr style="background:#f1f5f9;">
                            <th style="padding:8px 6px;">Date</th>
                            <th style="padding:8px 6px;">Day</th>
                            <th style="padding:8px 6px;">Employee Name</th>
                            <th style="padding:8px 6px;">Department</th>
                            <th style="padding:8px 6px;">Sub-Department</th>
                            <th style="padding:8px 6px;">In Time</th>
                            <th style="padding:8px 6px;">Out Time</th>
                        </tr>`;
                    const dateRef = logs.find(l => l.first_in);
                    let refDateObj = dateRef && dateRef.first_in ? new Date(dateRef.first_in.replace(' ', 'T')) : null;
                    let refDateStr = refDateObj ? refDateObj.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';
                    let refDayStr = refDateObj ? refDateObj.toLocaleDateString('en-US', { weekday: 'long' }) : '-';
                    logs.forEach(userAttendance => {
                        let dateObj = userAttendance.first_in ? new Date(userAttendance.first_in.replace(' ', 'T')) : null;
                        let dateStr = dateObj ? dateObj.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : refDateStr;
                        let dayStr = dateObj ? dateObj.toLocaleDateString('en-US', { weekday: 'long' }) : refDayStr;
                        let inTime = userAttendance.first_in || '<span style="color:#e11d48;font-weight:bold;">ABSENT</span>';
                        let outTime = userAttendance.last_out || '<span style="color:#e11d48;font-weight:bold;">ABSENT</span>';
                        html += `<tr>
                            <td style="padding:8px 6px;">${dateStr}</td>
                            <td style="padding:8px 6px;">${dayStr}</td>
                            <td style="padding:8px 6px;">${userAttendance.username || '-'}</td>
                            <td style="padding:8px 6px;">${userAttendance.department || '-'}</td>
                            <td style="padding:8px 6px;">${userAttendance.sub_department || '-'}</td>
                            <td style="padding:8px 6px;">${inTime}</td>
                            <td style="padding:8px 6px;">${outTime}</td>
                        </tr>`;
                    });
                    html += '</table></div>';
                } else if ((Array.isArray(logs) && logs.length > 0 && user.is_admin === true && (empId || summaryDate)) || (logs && logs.username)) {
                    // If filtered, show filtered user's attendance (handle both array and object response)
                    let filteredUser = Array.isArray(logs) ? logs[0] : logs;
                    let dateObj = filteredUser.first_in ? new Date(filteredUser.first_in.replace(' ', 'T')) : null;
                    let dateStr = dateObj ? dateObj.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';
                    let dayStr = dateObj ? dateObj.toLocaleDateString('en-US', { weekday: 'long' }) : '-';
                    // Format: {emp_id}_{username} Attendance Details
                    let headerEmpId = filteredUser.emp_id || filteredUser.employee_id || '';
                    let headerUsername = filteredUser.username || '';
                    let header = headerEmpId && headerUsername ? `${headerEmpId}-${headerUsername} Attendance Details` : (headerEmpId ? `${headerEmpId} Attendance Details` : (headerUsername ? `${headerUsername} Attendance Details` : 'Attendance Details'));
                    html += `<h3>${header}</h3>`;
                    html += `<div style="overflow-x:auto;"><table style="min-width:700px;width:100%;border-collapse:collapse;word-break:break-word;">
                        <tr style="background:#f1f5f9;">
                            <th style="padding:8px 6px;">Date</th>
                            <th style="padding:8px 6px;">Day</th>
                            <th style="padding:8px 6px;">Employee Name</th>
                            <th style="padding:8px 6px;">Department</th>
                            <th style="padding:8px 6px;">Sub-Department</th>
                            <th style="padding:8px 6px;">In Time</th>
                            <th style="padding:8px 6px;">Out Time</th>
                        </tr>
                        <tr>
                            <td style="padding:8px 6px;">${dateStr}</td>
                            <td style="padding:8px 6px;">${dayStr}</td>
                            <td style="padding:8px 6px;">${filteredUser.username || '-'}</td>
                            <td style="padding:8px 6px;">${filteredUser.department || '-'}</td>
                            <td style="padding:8px 6px;">${filteredUser.sub_department || '-'}</td>
                            <td style="padding:8px 6px;">${filteredUser.first_in || '<span style=\"color:#e11d48;font-weight:bold;\">ABSENT</span>'}</td>
                            <td style="padding:8px 6px;">${filteredUser.last_out || '<span style=\"color:#e11d48;font-weight:bold;\">ABSENT</span>'}</td>
                        </tr>
                    </table></div>`;
                } else {
                    // Find the current user's attendance summary
                    const userAttendance = Array.isArray(logs) ? logs.find(l => l.username === user.username) : logs;
                    html += '<h3>Your Attendance</h3>';
                    if (!userAttendance) {
                        html += '<p>No attendance records found.</p>';
                    } else {
                        let dateObj = userAttendance.first_in ? new Date(userAttendance.first_in.replace(' ', 'T')) : null;
                        let dateStr = dateObj ? dateObj.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';
                        let dayStr = dateObj ? dateObj.toLocaleDateString('en-US', { weekday: 'long' }) : '-';
                        html += `<div style="overflow-x:auto;"><table style="min-width:700px;width:100%;border-collapse:collapse;word-break:break-word;">
                            <tr style="background:#f1f5f9;">
                                <th style="padding:8px 6px;">Date</th>
                                <th style="padding:8px 6px;">Day</th>
                                <th style="padding:8px 6px;">Employee Name</th>
                                <th style="padding:8px 6px;">Department</th>
                                <th style="padding:8px 6px;">Sub-Department</th>
                                <th style="padding:8px 6px;">In Time</th>
                                <th style="padding:8px 6px;">Out Time</th>
                            </tr>
                            <tr>
                                <td style="padding:8px 6px;">${dateStr}</td>
                                <td style="padding:8px 6px;">${dayStr}</td>
                                <td style="padding:8px 6px;">${userAttendance.username || '-'}</td>
                                <td style="padding:8px 6px;">${userAttendance.department || '-'}</td>
                                <td style="padding:8px 6px;">${userAttendance.sub_department || '-'}</td>
                                <td style="padding:8px 6px;">${userAttendance.first_in || '-'}</td>
                                <td style="padding:8px 6px;">${userAttendance.last_out || '-'}</td>
                            </tr>
                        </table></div>`;
                    }
                }
                document.getElementById('attendanceSection').innerHTML = html;
            });
        }
        // Initial fetch
        fetchAndRenderAttendance();
        // Filter form logic (admin only)
        if (user.is_admin === true) {
            document.getElementById('filterForm').onsubmit = function(e) {
                e.preventDefault();
                const empId = document.getElementById('filterEmpId').value.trim();
                const summaryDate = document.getElementById('filterDate').value;
                fetchAndRenderAttendance(empId, summaryDate);
            };
            document.getElementById('clearFilterBtn').onclick = function() {
                document.getElementById('filterEmpId').value = '';
                document.getElementById('filterDate').value = '';
                fetchAndRenderAttendance();
            };
        }
    });
    // Logout
    document.getElementById('logoutBtn').onclick = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = 'login.html';
    };
    // Periodic refresh (e.g., every 15 minutes for 30 min expiry)
    setInterval(() => {
        refreshAccessToken().catch(() => {
            // On refresh failure, log out the user and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            alert('Session expired. Please log in again.');
            window.location.href = 'login.html';
        });
    }, 15 * 60 * 1000); // refresh and update access token every 15 minutes
}
