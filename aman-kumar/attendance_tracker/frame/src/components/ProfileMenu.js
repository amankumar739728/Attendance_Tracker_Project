import React, { useEffect, useState } from 'react';
import { IconButton, Menu, MenuItem, Avatar, Typography, Divider, Button, Alert, Snackbar } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import EditIcon from '@mui/icons-material/Edit';
import { getCurrentUser, updateUser } from '../api/user';
import { useNavigate } from 'react-router-dom';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { useUserUpdate } from './UserUpdateContext';

export default function ProfileMenu({ onLogout }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [user, setUser] = useState(null);
  const [editOpen, setEditOpen] = useState(false);
  const [editData, setEditData] = useState({ emp_id: '', email: '', department: '', sub_department: '' });
  const [notification, setNotification] = useState(null);
  const [notificationType, setNotificationType] = useState('success');
  const open = Boolean(anchorEl);
  const navigate = useNavigate();
  const { notifyUserUpdated, subscribe } = useUserUpdate();

  useEffect(() => {
    getCurrentUser().then(u => {
      setUser(u);
      setEditData({
        emp_id: u?.emp_id || '',
        email: u?.email || '',
        department: u?.department || '',
        sub_department: u?.sub_department || ''
      });
    }).catch(() => {});
    // Subscribe to user update events (e.g., from UserManagement)
    const unsubscribe = subscribe(() => {
      getCurrentUser().then(u => {
        setUser(u);
        setEditData({
          emp_id: u?.emp_id || '',
          email: u?.email || '',
          department: u?.department || '',
          sub_department: u?.sub_department || ''
        });
      });
    });
    return () => {
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, [subscribe]);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleUserMgmt = () => {
    handleClose();
    if (window.location.pathname === '/users') {
      window.location.reload();
    } else {
      navigate('/users');
    }
  };
  const handleLogoutClick = () => {
    handleClose();
    if (onLogout) onLogout();
  };
  const handleEditOpen = () => {
    // Always fetch the latest user data before opening the edit dialog
    getCurrentUser().then(u => {
      setUser(u);
      setEditData({
        emp_id: u?.emp_id || '',
        email: u?.email || '',
        department: u?.department || '',
        sub_department: u?.sub_department || ''
      });
      setEditOpen(true);
    });
  };
  const handleEditClose = () => {
    setEditOpen(false);
  };
  const handleEditChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };
  const handleEditSave = async () => {
    try {
      await updateUser(user.username, editData);
      setUser({ ...user, ...editData });
      setNotification('Profile updated successfully!');
      setNotificationType('success');
      setEditOpen(false);
      notifyUserUpdated(); // Notify other components (like UserManagement) to refresh
    } catch (err) {
      setNotification('Failed to update profile.');
      setNotificationType('error');
    }
  };

  return (
    <>
      <IconButton onClick={handleMenu} color="inherit">
        <Avatar>
          <AccountCircleIcon />
        </Avatar>
      </IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem disabled sx={{ bgcolor: '#fff' }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#111', letterSpacing: 0.5 }}>Your Profile</Typography>
        </MenuItem>
        {user && (
          <MenuItem disabled sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 0.5, bgcolor: '#fff' }}>
            <Typography variant="subtitle1" fontWeight={700} color="#000">{user.username}</Typography>
            <Typography variant="body2" color="#000">{user.email}</Typography>
            <Typography variant="body2" color="#000">{user.department} / {user.sub_department}</Typography>
            <Typography variant="body2" color="#444">{user.is_admin ? 'Admin' : 'User'}</Typography>
          </MenuItem>
        )}
        <MenuItem onClick={handleEditOpen} sx={{ color: '#2563eb', fontWeight: 600 }}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} /> Edit Profile
        </MenuItem>
        <MenuItem onClick={() => { handleClose(); navigate('/change-password'); }} sx={{ color: '#2563eb', fontWeight: 600 }}>
          Change Password
        </MenuItem>
        <Divider />
        {user && user.is_admin && (
          <MenuItem onClick={handleUserMgmt}>User Management</MenuItem>
        )}
        <MenuItem onClick={handleLogoutClick}>Logout</MenuItem>
      </Menu>
      <Dialog open={editOpen} onClose={handleEditClose} maxWidth="xs" fullWidth scroll="paper">
        <DialogTitle>Edit Profile</DialogTitle>
        <DialogContent dividers sx={{
          display: 'flex', flexDirection: 'column', gap: 2, mt: 1,
          maxHeight: 350, minHeight: 200, overflowY: 'auto',
          // Ensure scrollability on all devices
        }}>
          <TextField label="emp_id" name="emp_id" value={editData.emp_id} onChange={handleEditChange} fullWidth size="small" />
          <TextField label="Email" name="email" value={editData.email} onChange={handleEditChange} fullWidth size="small" />
          <TextField label="Department" name="department" value={editData.department} onChange={handleEditChange} fullWidth size="small" />
          <TextField label="Sub-Department" name="sub_department" value={editData.sub_department} onChange={handleEditChange} fullWidth size="small" />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleEditClose} color="inherit">Cancel</Button>
          <Button onClick={handleEditSave} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={!!notification}
        autoHideDuration={4000}
        onClose={() => setNotification(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert onClose={() => setNotification(null)} severity={notificationType} sx={{ width: '100%' }}>
          {notification}
        </Alert>
      </Snackbar>
    </>
  );
}
