import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Register from './components/Register';
import UserManagement from './components/UserManagement';
import { getAccessToken, logout } from './api/auth';
import { startPeriodicTokenRefresh } from './api/token';
import { UserUpdateProvider } from './components/UserUpdateContext';
import ChangePassword from './components/ChangePassword';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import LandingPage from './components/LandingPage';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!getAccessToken());

  const handleLogin = () => setIsLoggedIn(true);
  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
  };

  React.useEffect(() => {
    startPeriodicTokenRefresh(); // Start periodic token refresh on app mount
  }, []);

  return (
    <UserUpdateProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={isLoggedIn ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/" />} />
          <Route path="/users" element={isLoggedIn ? <UserManagement onLogout={handleLogout} /> : <Navigate to="/" />} />
          <Route path="/change-password" element={isLoggedIn ? <ChangePassword /> : <Navigate to="/login" />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="*" element={<Navigate to={isLoggedIn ? "/dashboard" : "/login"} />} />
        </Routes>
      </Router>
    </UserUpdateProvider>
  );
}

export default App;
