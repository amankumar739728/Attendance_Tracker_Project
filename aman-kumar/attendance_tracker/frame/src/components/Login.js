import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Alert,
  FormControlLabel,
  Checkbox,
  IconButton,
  InputAdornment,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  DarkMode,
  LightMode,
} from '@mui/icons-material';
import { login } from '../api/auth';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [darkMode, setDarkMode] = useState(() =>
    document.documentElement.classList.contains('dark')
  );
  const navigate = useNavigate();

  useEffect(() => {
    const savedUsername = localStorage.getItem('rememberedUsername');
    if (savedUsername) {
      setUsername(savedUsername);
      setRememberMe(true);
    }
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (rememberMe) {
        localStorage.setItem('rememberedUsername', username);
      } else {
        localStorage.removeItem('rememberedUsername');
      }
      await login(username, password);
      if (onLogin) onLogin();
      navigate('/dashboard', { state: { showLoginSuccess: true } });
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleDarkMode = () => setDarkMode((prev) => !prev);

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
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            minWidth: 320,
            bgcolor: darkMode ? '#18181b' : 'background.paper',
            color: darkMode ? '#fff' : 'text.primary',
            borderRadius: 4,
            boxShadow: 8,
          }}
        >
          <Typography
            variant="h4"
            align="center"
            color="primary"
            fontWeight="bold"
            mb={2}
          >
            Login
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              fullWidth
              margin="normal"
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <i className="fas fa-user" style={{ color: '#a78bfa' }}></i>
                  </InputAdornment>
                ),
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
              label="Password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
              margin="normal"
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <i className="fas fa-lock" style={{ color: '#a78bfa' }}></i>
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword((show) => !show)}
                      edge="end"
                      size="small"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
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
            <Box
              display="flex"
              alignItems="center"
              justifyContent="space-between"
              mt={1}
              mb={2}
            >
              <FormControlLabel
                control={
                  <Checkbox
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    color="primary"
                  />
                }
                label={<Typography variant="body2">Remember Me</Typography>}
              />
              <Typography
                variant="body2"
                color="primary"
                sx={{ cursor: 'pointer', textDecoration: 'underline' }}
                onClick={() => navigate('/forgot-password')}
              >
                Forgot password?
              </Typography>
            </Box>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              disabled={loading}
              sx={{ mt: 1, fontWeight: 'bold', fontSize: 16 }}
            >
              {loading ? 'Logging in...' : 'Login'}
            </Button>
          </form>
          <Typography align="center" variant="body2" mt={2}>
            Don't have an account?{' '}
            <span
              style={{
                color: '#a78bfa',
                cursor: 'pointer',
                textDecoration: 'underline',
              }}
              onClick={() => navigate('/register')}
            >
              Register
            </span>
          </Typography>
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
        </Paper>
      </motion.div>
    </Box>
  );
}
