import React, { useEffect, useState } from 'react';
import {
  Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert, Button, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, TextField
} from '@mui/material';
import { getAllUsers, updateUser, deleteUser, getUserByUsername, getUserByEmpId } from '../api/user';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AddIcon from '@mui/icons-material/Add';
import { useNavigate } from 'react-router-dom';
import ProfileMenu from './ProfileMenu';
import { useUserUpdate } from './UserUpdateContext';

export default function UserManagement({ onLogout }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dialogType, setDialogType] = useState(''); // 'edit', 'view', 'register'
  const [form, setForm] = useState({});
  const [formError, setFormError] = useState('');
  const [formLoading, setFormLoading] = useState(false);
  const [notification, setNotification] = useState("");
  const [deleteDialog, setDeleteDialog] = useState({ open: false, user: null });
  const [page, setPage] = useState(1);
  const rowsPerPage = 5;
  const [searchUsername, setSearchUsername] = useState('');
  const [searchError, setSearchError] = useState('');
  const [searchLoading, setSearchLoading] = useState(false);
  const navigate = useNavigate();
  const { subscribe, notifyUserUpdated } = useUserUpdate();

  const fetchUsers = () => {
    setLoading(true);
    getAllUsers()
      .then(users => {
        // Sort: root user first, then by emp_id ascending
        const sorted = [...users].sort((a, b) => {
          if (a.username === 'root') return -1;
          if (b.username === 'root') return 1;
          // If emp_id is numeric, compare as numbers, else as strings
          const aEmp = isNaN(Number(a.emp_id)) ? a.emp_id : Number(a.emp_id);
          const bEmp = isNaN(Number(b.emp_id)) ? b.emp_id : Number(b.emp_id);
          if (aEmp < bEmp) return -1;
          if (aEmp > bEmp) return 1;
          return 0;
        });
        setUsers(sorted);
      })
      .catch(() => setError('Failed to fetch users'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchUsers();
    // Subscribe to user update events (e.g., from ProfileMenu)
    const unsubscribe = subscribe(() => {
      fetchUsers();
    });
    return () => unsubscribe();
  }, [subscribe]);

  const handleEdit = (user) => {
    setForm({ ...user });
    setDialogType('edit');
    setFormError('');
  };
  const handleView = async (user) => {
    setFormLoading(true);
    try {
      const data = await getUserByUsername(user.username);
      setForm({ ...data }); // <-- Set form with fetched user data
      setDialogType('view');
    } catch {
      setFormError('Failed to fetch user details');
    } finally {
      setFormLoading(false);
    }
  };
  const handleDelete = (user) => {
    setDeleteDialog({ open: true, user });
  };
  const confirmDelete = async () => {
    setFormLoading(true);
    try {
      await deleteUser(deleteDialog.user.username);
      fetchUsers();
      setNotification(`User ${deleteDialog.user.username} deleted successfully!`);
      setTimeout(() => setNotification(""), 4000);
    } catch {
      setError('Failed to delete user');
    } finally {
      setFormLoading(false);
      setDeleteDialog({ open: false, user: null });
    }
  };
  const cancelDelete = () => {
    setDeleteDialog({ open: false, user: null });
  };
  const handleRegister = () => {
    setForm({ emp_id: '', username: '', email: '', password: '', department: '', sub_department: '', is_admin: false });
    setDialogType('register');
    setFormError('');
  };
  const handleDialogClose = () => {
    setDialogType('');
    setForm({});
    setFormError('');
    setSearchError('');
  };
  const handleFormChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    setFormLoading(true);
    try {
      if (dialogType === 'edit') {
        await updateUser(form.username, form);
        await fetchUsers();
        notifyUserUpdated(); // Notify ProfileMenu to refresh
        setNotification(`Details have been updated for ${form.username}.`);
        setTimeout(() => setNotification(""), 4000);
        handleDialogClose();
      } else if (dialogType === 'register') {
        const res = await fetch('http://localhost:9123/v1/user/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form)
        });
        const data = await res.json();
        if (res.ok) {
          await fetchUsers();
          notifyUserUpdated(); // Notify ProfileMenu to refresh
          setNotification(`Username: ${form.username} created successfully!`);
          setTimeout(() => setNotification(""), 4000);
          handleDialogClose();
        } else {
          setFormError(data.detail || 'Registration failed.');
        }
      }
    } catch {
      setFormError('Failed to submit form');
    } finally {
      setFormLoading(false);
    }
  };

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchUsername(value);
    if (!value.trim()) {
      setSearchError('');
      fetchUsers();
      return;
    }
    setSearchLoading(true);
    setSearchError('');
    const isNumeric = /^\d+$/.test(value.trim());
    const fetchFunc = isNumeric ? getUserByEmpId : getUserByUsername;
    fetchFunc(value.trim())
      .then(user => {
        setUsers(user ? [user] : []);
        setPage(1);
      })
      .catch(() => {
        setSearchError('User not found.');
        setUsers([]);
      })
      .finally(() => {
        setSearchLoading(false);
      });
  };

  const handleSearch = async () => {
    if (!searchUsername.trim()) {
      setSearchError('Please enter a username or Employee ID to search.');
      return;
    }
    setSearchLoading(true);
    setSearchError('');
    try {
      const user = await getUserByUsername(searchUsername.trim());
      setUsers(user ? [user] : []);
      setPage(1);
    } catch {
      setSearchError(`User not found.`);
      setUsers([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchUsername('');
    setSearchError('');
    fetchUsers();
  };

  // Pagination logic similar to Dashboard
  const paginatedUsers = users.slice((page - 1) * rowsPerPage, page * rowsPerPage);
  const pageCount = Math.max(1, Math.ceil(users.length / rowsPerPage));

  return (
    <Box p={4}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">User Management</Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <Button variant="outlined" onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleRegister}>Add User</Button>
          <ProfileMenu onLogout={onLogout} />
        </Box>
      </Box>
      {notification && (
        <Alert severity="success" sx={{ mb: 2 }}>{notification}</Alert>
      )}
      <Box mb={2} display="flex" alignItems="center" gap={2}>
        <TextField
          label="Search by Username or emp_id"
          value={searchUsername}
          onChange={handleSearchChange}
          size="small"
          error={!!searchError}
          helperText={searchError}
        />
        <Button variant="contained" color="primary" onClick={handleSearch} disabled={searchLoading}>
          Search
        </Button>
        <Button variant="outlined" sx={{ borderColor: 'rgba(0, 0, 0, 0.23)' }} onClick={handleClearSearch} disabled={searchLoading}>
          Clear
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <>
          <TableContainer component={Paper} sx={{ mt: 2, borderRadius: 3, boxShadow: 6, border: '1px solid #e0e0e0', background: theme => theme.palette.mode === 'dark' ? '#23272f' : '#f8fafc' }}>
            <Table sx={{ minWidth: 700 }}>
              <TableHead>
                <TableRow sx={{ background: theme => theme.palette.mode === 'dark' ? '#18181b' : '#ede9fe' }}>
                  <TableCell>Employee ID</TableCell>
                  <TableCell>Username</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Department</TableCell>
                  <TableCell>Sub-Department</TableCell>
                  <TableCell>Admin</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedUsers.map((user, idx) => (
                  <TableRow key={idx}>
                    <TableCell>{user.emp_id}</TableCell>
                    <TableCell>{user.username}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>{user.department}</TableCell>
                    <TableCell>{user.sub_department}</TableCell>
                    <TableCell>{user.is_admin ? 'Yes' : 'No'}</TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleView(user)}><VisibilityIcon /></IconButton>
                      <IconButton onClick={() => handleEdit(user)}><EditIcon /></IconButton>
                      <IconButton onClick={() => handleDelete(user)} disabled={user.username === 'root'}><DeleteIcon /></IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Box display="flex" justifyContent="center" mt={2}>
            <Button
              onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
              disabled={page === 1}
              variant="outlined"
              sx={{ mx: 1 }}
            >
              Prev
            </Button>
            <Typography variant="body2" sx={{ mx: 2, mt: 1 }}>{page} / {pageCount}</Typography>
            <Button
              onClick={() => setPage((prev) => Math.min(prev + 1, pageCount))}
              disabled={page === pageCount}
              variant="outlined"
              sx={{ mx: 1 }}
            >
              Next
            </Button>
          </Box>
        </>
      )}
      {/* Dialog for view/edit/register */}
      <Dialog open={!!dialogType} onClose={handleDialogClose} maxWidth="xs" fullWidth>
        <DialogTitle>
          {dialogType === 'edit' && 'Edit User'}
          {dialogType === 'view' && 'User Details'}
          {dialogType === 'register' && 'Register New User'}
        </DialogTitle>
        <DialogContent>
          {formLoading ? <CircularProgress /> : (
            <form onSubmit={handleFormSubmit} id="userForm">
              <TextField label="Employee ID" name="emp_id" value={form.emp_id || ''} onChange={handleFormChange} fullWidth margin="normal" required disabled={dialogType === 'view'} />
              <TextField label="Username" name="username" value={form.username || ''} onChange={handleFormChange} fullWidth margin="normal" required disabled={dialogType === 'view' || dialogType === 'edit'} />
              <TextField label="Email" name="email" value={form.email || ''} onChange={handleFormChange} fullWidth margin="normal" required disabled={dialogType === 'view'} />
              {dialogType === 'register' && <TextField label="Password" name="password" type="password" value={form.password || ''} onChange={handleFormChange} fullWidth margin="normal" required />}
              <TextField label="Department" name="department" value={form.department || ''} onChange={handleFormChange} fullWidth margin="normal" required disabled={dialogType === 'view'} />
              <TextField label="Sub-Department" name="sub_department" value={form.sub_department || ''} onChange={handleFormChange} fullWidth margin="normal" required disabled={dialogType === 'view'} />
              <TextField
                select
                label="Admin"
                name="is_admin"
                value={form.is_admin ? 'Yes' : 'No'}
                onChange={e => setForm({ ...form, is_admin: e.target.value === 'Yes' })}
                fullWidth
                margin="normal"
                required
                disabled={dialogType === 'view'}
                SelectProps={{ native: true }}
              >
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </TextField>
              {formError && <Alert severity="error" sx={{ mt: 1 }}>{formError}</Alert>}
            </form>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Close</Button>
          {dialogType !== 'view' && <Button type="submit" form="userForm" variant="contained" disabled={formLoading}>{dialogType === 'edit' ? 'Save' : 'Register'}</Button>}
        </DialogActions>
      </Dialog>
      {/* Delete confirmation dialog */}
      <Dialog open={deleteDialog.open} onClose={cancelDelete}>
        <DialogTitle>Delete User</DialogTitle>
        <DialogContent>
          <Typography>Do you want to delete user: <b>{deleteDialog.user?.username}</b>?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={cancelDelete} color="primary">No</Button>
          <Button onClick={confirmDelete} color="error" disabled={formLoading}>Yes</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
