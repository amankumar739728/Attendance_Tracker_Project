import React, { useState, useEffect } from 'react';
import { TextField, Button, Typography, Box, Alert, Snackbar } from '@mui/material';
import { resetPassword } from '../api/user';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { DarkMode, LightMode } from '@mui/icons-material';

export default function ResetPassword() {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [notification, setNotification] = useState(null);
  const [notificationType, setNotificationType] = useState('success');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(() =>
    document.documentElement.classList.contains('dark')
  );
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setDarkMode(savedTheme === 'dark');
    } else {
      const prefersDark =
        window.matchMedia &&
        window.matchMedia('(prefers-color-scheme: dark)').matches;
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

  const handleToggleDarkMode = () => setDarkMode((prev) => !prev);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setNotificationType('error');
      setNotification('New password and confirm password do not match.');
      return;
    }
    if (!token) {
      setNotificationType('error');
      setNotification('Invalid or missing token.');
      return;
    }
    setLoading(true);
    setNotification(null);
    try {
      await resetPassword(token, newPassword);
      setNotificationType('success');
      setNotification('Password reset successfully. Redirecting to login...');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setNotificationType('error');
      setNotification(error.message || 'Failed to reset password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      sx={{
        background: darkMode
          ? 'linear-gradient(to bottom right, #111827, #6d28d9, #1f2937)'
          : 'linear-gradient(to bottom right, #f5f6fa, #ede9fe, #e0e7ff)',
      }}
    >
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          maxWidth: 400,
          mx: 'auto',
          mt: 4,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          bgcolor: darkMode ? '#18181b' : 'background.paper',
          color: darkMode ? '#fff' : 'text.primary',
          borderRadius: 4,
          boxShadow: 8,
          p: 4,
          minWidth: 320,
        }}
      >
        <Typography variant="h5" component="h1" gutterBottom>
          Reset Password
        </Typography>
        <TextField
          label="New Password"
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
          fullWidth
          InputProps={{
            style: {
              color: darkMode ? '#fff' : undefined,
              background: darkMode ? '#23232a' : undefined,
            },
          }}
          InputLabelProps={{
            style: { color: darkMode ? '#a78bfa' : undefined },
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              '& fieldset': {
                borderColor: darkMode ? '#a78bfa' : undefined,
              },
              '&:hover fieldset': {
                borderColor: darkMode ? '#c4b5fd' : undefined,
              },
              '&.Mui-focused fieldset': {
                borderColor: darkMode ? '#c4b5fd' : undefined,
              },
              background: darkMode ? '#23232a' : undefined,
              color: darkMode ? '#fff' : undefined,
            },
            input: { color: darkMode ? '#fff' : undefined },
          }}
        />
        <TextField
          label="Confirm New Password"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          fullWidth
          InputProps={{
            style: {
              color: darkMode ? '#fff' : undefined,
              background: darkMode ? '#23232a' : undefined,
            },
          }}
          InputLabelProps={{
            style: { color: darkMode ? '#a78bfa' : undefined },
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              '& fieldset': {
                borderColor: darkMode ? '#a78bfa' : undefined,
              },
              '&:hover fieldset': {
                borderColor: darkMode ? '#c4b5fd' : undefined,
              },
              '&.Mui-focused fieldset': {
                borderColor: darkMode ? '#c4b5fd' : undefined,
              },
              background: darkMode ? '#23232a' : undefined,
              color: darkMode ? '#fff' : undefined,
            },
            input: { color: darkMode ? '#fff' : undefined },
          }}
        />
        <Button type="submit" variant="contained" color="primary" disabled={loading}>
          {loading ? 'Resetting...' : 'Reset Password'}
        </Button>
        <Button variant="text" onClick={() => navigate('/login')}>
          Back to Login
        </Button>
        <Box display="flex" justifyContent="center" mt={3}>
          <Button
            onClick={handleToggleDarkMode}
            color="secondary"
            startIcon={darkMode ? <LightMode /> : <DarkMode />}
            sx={{ textTransform: 'none' }}
          >
            Toggle Dark Mode
          </Button>
        </Box>
        <Snackbar
          open={!!notification}
          autoHideDuration={4000}
          onClose={() => setNotification(null)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert onClose={() => setNotification(null)} severity={notificationType} sx={{ width: '100%' }}>
            {notification}
          </Alert>
        </Snackbar>
      </Box>
    </Box>
  );
}
