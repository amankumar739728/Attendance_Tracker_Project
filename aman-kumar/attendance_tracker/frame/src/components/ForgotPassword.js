import React, { useState, useEffect } from 'react';
import { TextField, Button, Typography, Box, Alert, Snackbar } from '@mui/material';
import { forgotPassword } from '../api/user';
import { useNavigate } from 'react-router-dom';
import { DarkMode, LightMode } from '@mui/icons-material';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [notification, setNotification] = useState(null);
  const [notificationType, setNotificationType] = useState('success');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(() =>
    document.documentElement.classList.contains('dark')
  );
  const navigate = useNavigate();

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
    setLoading(true);
    setNotification(null);
    try {
      await forgotPassword(email);
      setNotificationType('success');
      setNotification('Password reset email sent. Please check your inbox.');
      setEmail('');
      // Optionally navigate to reset password page or login page
      // navigate('/reset-password');
    } catch (error) {
      setNotificationType('error');
      setNotification(error.message || 'Failed to send password reset email.');
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
          Forgot Password
        </Typography>
        <Typography variant="body2" gutterBottom>
          Enter your email address to receive a password reset link.
        </Typography>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
          {loading ? 'Sending...' : 'Send Reset Email'}
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
