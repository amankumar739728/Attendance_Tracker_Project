import React, { useState, useEffect } from 'react';
import { Box, Button, TextField, Typography, Paper, Alert, InputAdornment, IconButton } from '@mui/material';
import { Visibility, VisibilityOff, DarkMode, LightMode } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const [form, setForm] = useState({
    emp_id: '', username: '', email: '', password: '', department: '', sub_department: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [darkMode, setDarkMode] = useState(() => document.documentElement.classList.contains('dark'));
  const navigate = useNavigate();

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setDarkMode(savedTheme === 'dark');
    } else {
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      setDarkMode(prefersDark);
    }
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const res = await fetch('https://attendance-tracker-project.onrender.com/v1/user/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, is_admin: false })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess('Registration successful! Please login.');
        setForm({ emp_id: '', username: '', email: '', password: '', department: '', sub_department: '' });
      } else {
        setError(data.detail || 'Registration failed.');
      }
    } catch (err) {
      setError('Server error.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleDarkMode = () => setDarkMode(prev => !prev);

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh"
      sx={{
        background: darkMode
          ? 'linear-gradient(to bottom right, #111827, #6d28d9, #1f2937)'
          : 'linear-gradient(to bottom right, #f5f6fa, #ede9fe, #e0e7ff)'
      }}
    >
      <Paper elevation={3} sx={{
        p: 4,
        maxWidth: 400,
        width: '100%',
        bgcolor: darkMode ? '#18181b' : 'background.paper',
        color: darkMode ? '#fff' : 'text.primary',
        borderRadius: 4,
        boxShadow: 8
      }}>
        <Typography variant="h4" align="center" color="primary" fontWeight="bold" mb={2}>
          Register
        </Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
        <form onSubmit={handleSubmit}>
          <Box display="flex" gap={2}>
            <TextField
              label="Employee ID"
              name="emp_id"
              value={form.emp_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.emp_id
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
            <TextField
              label="Username"
              name="username"
              value={form.username}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <i className="fas fa-user" style={{ color: '#a78bfa' }}></i>
                  </InputAdornment>
                )
              }}
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.username
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
          </Box>
          <Box display="flex" gap={2}>
            <TextField
              label="Email"
              name="email"
              value={form.email}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.email
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
            <TextField
              label="Password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={form.password}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <i className="fas fa-lock" style={{ color: '#a78bfa' }}></i>
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword((show) => !show)} edge="end" size="small">
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                )
              }}
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.password
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
          </Box>
          <Box display="flex" gap={2}>
            <TextField
              label="Department"
              name="department"
              value={form.department}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.department
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
            <TextField
              label="Sub-Department"
              name="sub_department"
              value={form.sub_department}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              variant="outlined"
              InputLabelProps={{
                style: { color: darkMode ? '#a78bfa' : undefined },
                shrink: !!form.sub_department
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  background: darkMode ? '#23232a' : undefined,
                  color: darkMode ? '#fff' : undefined
                },
                input: { color: darkMode ? '#fff' : undefined }
              }}
            />
          </Box>
          <Button type="submit" variant="contained" color="primary" fullWidth disabled={loading}
            sx={{ mt: 2, fontWeight: 'bold', fontSize: 16 }}>
            {loading ? 'Registering...' : 'Register'}
          </Button>
        </form>
        <Typography align="center" variant="body2" mt={2}>
          Already have an account?{' '}
          <span style={{ color: '#a78bfa', cursor: 'pointer', textDecoration: 'underline' }} onClick={() => navigate('/login')}>
            Login
          </span>
        </Typography>
        <Box display="flex" justifyContent="center" mt={3}>
          <Button onClick={handleToggleDarkMode} color="secondary" startIcon={darkMode ? <LightMode /> : <DarkMode />} sx={{ textTransform: 'none' }}>
            Toggle Dark Mode
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
