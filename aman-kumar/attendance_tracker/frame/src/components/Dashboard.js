import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, TextField, MenuItem, Select, FormControl, InputLabel, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import ProfileMenu from './ProfileMenu';
import AttendanceTable from './AttendanceTable';
import { getCurrentUser } from '../api/user';
import { getAttendanceSummary, deleteAttendanceByEmpIdAndDay, punchAttendance } from '../api/attendance';
import { format } from 'date-fns';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useUserUpdate } from './UserUpdateContext';

export default function Dashboard({ onLogout }) {
  const [user, setUser] = useState(null);
  const [attendance, setAttendance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterEmpId, setFilterEmpId] = useState('');
  const [filterDate, setFilterDate] = useState('');
  // For non-admins: form for emp_id/username and date
  const [userInput, setUserInput] = useState("");
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });
  const [mode, setMode] = useState('get'); // 'get' or 'delete'
  const [deleteEmpId, setDeleteEmpId] = useState('');
  const [deleteDate, setDeleteDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [punchLoading, setPunchLoading] = useState(false);
  // Confirmation dialog state for delete attendance
  const [deleteConfirmDialog, setDeleteConfirmDialog] = useState({ open: false, empId: '' });
  // Pagination and sorting for admin view
  const [page, setPage] = useState(1);
  const rowsPerPage = 5;
  let sortedAttendance = attendance;
  const location = useLocation();
  const [showLoginSuccess, setShowLoginSuccess] = useState(false);
  const { subscribe } = useUserUpdate();

  useEffect(() => {
    // Set default date to today
    const today = format(new Date(), 'yyyy-MM-dd');
    setFilterDate(today);
    setDeleteDate(today);
    getCurrentUser().then(setUser).catch(() => setUser(null));
  }, []);

  useEffect(() => {
    if (user) {
      // Fetch attendance for today by default
      fetchAttendance(filterEmpId, filterDate || format(new Date(), 'yyyy-MM-dd'));
    }
    // eslint-disable-next-line
  }, [user]);

  useEffect(() => {
    if (location.state && location.state.showLoginSuccess) {
      setShowLoginSuccess(true);
      setTimeout(() => setShowLoginSuccess(false), 1800);
    }
  }, [location.state]);

  // Subscribe to user update events to refresh user and attendance data
  useEffect(() => {
    const unsubscribe = subscribe(() => {
      getCurrentUser().then(setUser).then(() => {
        if (user) {
          fetchAttendance(filterEmpId, filterDate);
        }
      });
    });
    return () => unsubscribe();
  }, [subscribe, user, filterEmpId, filterDate]);

  const fetchAttendance = async (empId = '', date = '') => {
    setLoading(true);
    setError('');
    try {
      const data = await getAttendanceSummary(empId, date);
      if (!data || (Array.isArray(data) && data.length === 0)) {
        setError(`No attendance record available for ${empId}. Please hit clear and try with available emp_id`);
        setAttendance([]);
      } else {
        setAttendance(data);
      }
    } catch (err) {
      setError(`No attendance record available for ${empId}. Please hit clear and try with available emp_id`);
      setAttendance(null);
    } finally {
      setLoading(false);
    }
  };

  // Debounce function to limit frequency of function calls
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  const debouncedFetchAttendance = React.useRef(
    debounce((empId, date) => {
      fetchAttendance(empId, date);
    }, 500)
  ).current;

  // For non-admins: fetch attendance by emp_id or username
  const fetchAttendanceByInput = async (input, date) => {
    setLoading(true);
    setError("");
    try {
      let data;
      if (/^\d+$/.test(input)) {
        // All digits: treat as emp_id
        data = await import('../api/attendance').then(api => api.getAttendanceByEmpId(input, date));
      } else {
        // Otherwise, treat as username
        data = await import('../api/attendance').then(api => api.getAttendanceByUsername(input, date));
      }
      // If backend returns access restriction message, show notification
      if (data && data.message && data.message.includes('Access restricted')) {
        setNotification({ open: true, message: data.message, severity: 'warning' });
        setAttendance(null);
      } else {
        setAttendance([data]);
      }
    } catch (err) {
      setError('Failed to fetch attendance');
      setAttendance(null);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = (e) => {
    e.preventDefault();
    setError("");
    if (filterDate && isNaN(Date.parse(filterDate))) {
      setError("Invalid date format");
      return;
    }
    fetchAttendance(filterEmpId, filterDate);
  };

  // When emp_id is cleared, auto-fetch all attendance for the date
  const handleEmpIdChange = (e) => {
    const value = e.target.value;
    setFilterEmpId(value);
    if (value === "") {
      fetchAttendance("", filterDate);
    } else {
      debouncedFetchAttendance(value, filterDate);
    }
  };

  const handleDateChange = (e) => {
    const value = e.target.value;
    setFilterDate(value);
    // Immediately fetch attendance for the new date
    fetchAttendance(filterEmpId, value);
  };

  const handleClear = () => {
    const today = format(new Date(), 'yyyy-MM-dd');
    setFilterEmpId("");
    setFilterDate(today);
    setError("");
    fetchAttendance("", today);
  };

  // Non-admin filter handlers
  const handleNonAdminFilter = (e) => {
    e.preventDefault();
    setError("");
    if (!userInput || !filterDate) {
      setError("Both fields are required");
      return;
    }
    fetchAttendanceByInput(userInput, filterDate);
  };

  const handleNonAdminClear = () => {
    setUserInput("");
    const today = format(new Date(), 'yyyy-MM-dd');
    setFilterDate(today);
    setError("");
    // Fetch current user's attendance for today
    if (user) {
      fetchAttendanceByInput(user.emp_id, today);
    }
  };

  // Delete attendance handler
  const handleDeleteAttendance = async (e) => {
    e.preventDefault();
    // Open confirmation dialog instead of deleting immediately
    setDeleteConfirmDialog({ open: true, empId: deleteEmpId });
  };

  const confirmDeleteAttendance = async () => {
    setDeleteLoading(true);
    setError('');
    try {
      await deleteAttendanceByEmpIdAndDay(deleteConfirmDialog.empId, deleteDate);
      setNotification({ open: true, message: `Attendance for emp_id: ${deleteConfirmDialog.empId} is deleted for ${deleteDate}`, severity: 'success' });
      setDeleteEmpId('');
      // Refresh attendance data after deletion
      if (user) {
        if (user.is_admin) {
          fetchAttendance(filterEmpId, filterDate);
        } else {
          fetchAttendanceByInput(user.emp_id, filterDate);
        }
      }
    } catch (err) {
      setNotification({ open: true, message: 'Failed to delete attendance. Provide a valid emp_id', severity: 'error' });
    } finally {
      setDeleteLoading(false);
      setDeleteConfirmDialog({ open: false, empId: '' });
    }
  };

  const cancelDeleteAttendance = () => {
    setDeleteConfirmDialog({ open: false, empId: '' });
  };

  const handlePunch = async (action) => {
    setPunchLoading(true);
    try {
      await punchAttendance(action);
      setNotification({ open: true, message: `Attendance ${action === 'IN' ? 'In Time' : 'Out Time'} punched successfully!`, severity: 'success' });
      // Refresh attendance data after punch
      if (user) {
        if (user.is_admin) {
          fetchAttendance(filterEmpId, filterDate);
        } else {
          fetchAttendanceByInput(user.emp_id, filterDate);
        }
      }
    } catch (err) {
      setNotification({ open: true, message: `Failed to punch ${action === 'IN' ? 'In Time' : 'Out Time'}`, severity: 'error' });
    } finally {
      setPunchLoading(false);
    }
  };

  useEffect(() => {
    if (location.state && location.state.showLoginSuccess && user) {
      setNotification({ open: true, message: `Logged in as ${user.username}.`, severity: 'success' });
      // Remove the notification after 2 seconds
      setTimeout(() => setNotification({ open: false, message: '', severity: 'success' }), 2000);
    }
  }, [location.state, user]);

  if (user && user.is_admin && Array.isArray(attendance)) {
    sortedAttendance = [...attendance].sort((a, b) => {
      if (a.username === 'root') return -1;
      if (b.username === 'root') return 1;
      // Numeric sort for emp_id if possible, else string
      const aEmp = isNaN(Number(a.emp_id)) ? a.emp_id : Number(a.emp_id);
      const bEmp = isNaN(Number(b.emp_id)) ? b.emp_id : Number(b.emp_id);
      if (aEmp < bEmp) return -1;
      if (aEmp > bEmp) return 1;
      return 0;
    });
  }
  const paginatedAttendance = user && user.is_admin && Array.isArray(sortedAttendance)
    ? sortedAttendance.slice((page - 1) * rowsPerPage, page * rowsPerPage)
    : sortedAttendance;
  const pageCount = user && user.is_admin && Array.isArray(sortedAttendance)
    ? Math.ceil(sortedAttendance.length / rowsPerPage)
    : 1;

  return (
    <Box p={4}>
      <AnimatePresence>
        {showLoginSuccess && (
          <motion.div
            initial={{ opacity: 0, scale: 0.7 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.7 }}
            transition={{ duration: 0.5 }}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              width: '100vw',
              height: '100vh',
              background: 'rgba(0,0,0,0.15)',
              zIndex: 2000,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
              style={{
                background: '#fff',
                borderRadius: '50%',
                boxShadow: '0 4px 32px rgba(80,80,200,0.15)',
                padding: 40,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <motion.svg width="80" height="80" viewBox="0 0 80 80">
                <motion.circle cx="40" cy="40" r="38" stroke="#4ade80" strokeWidth="4" fill="none" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.5 }}/>
                <motion.path d="M25 42 L37 54 L56 32" stroke="#4ade80" strokeWidth="5" fill="none" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.7, delay: 0.2 }}/>
              </motion.svg>
              <Typography variant="h6" color="success.main" mt={2} fontWeight="bold">Login Successful!</Typography>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4" mb={3}>Dashboard</Typography>
        <Box display="flex" alignItems="center" gap={2}>
          {user && user.is_admin && (
            <Button variant="outlined" onClick={() => window.location.href = '/users'}>Go to User Management</Button>
          )}
          <ProfileMenu onLogout={onLogout} />
        </Box>
      </Box>

      {/* Attendance label and punch buttons at the top */}
      <Box display="flex" alignItems="center" gap={2} mb={4}>
        <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>Attendance:</Typography>
        <Button variant="contained" color="success" onClick={() => handlePunch('IN')} disabled={punchLoading}>Punch In</Button>
        <Button variant="contained" color="warning" onClick={() => handlePunch('OUT')} disabled={punchLoading}>Punch Out</Button>
      </Box>

      {/* Mode selector and filter controls */}
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        {user && user.is_admin && (
          <>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel id="mode-select-label">Mode</InputLabel>
              <Select
                labelId="mode-select-label"
                value={mode}
                label="Mode"
                onChange={e => setMode(e.target.value)}
              >
                <MenuItem value="get">Get</MenuItem>
                <MenuItem value="delete">Delete</MenuItem>
              </Select>
            </FormControl>
            {mode === 'get' && (
              <>
                <TextField label="Employee ID" value={filterEmpId} onChange={handleEmpIdChange} size="small" disabled={loading} />
                <TextField label="Date" type="date" value={filterDate} onChange={handleDateChange} size="small" InputLabelProps={{ shrink: true }} disabled={loading} />
                <Button type="button" variant="contained" onClick={handleFilter} disabled={loading}>Apply Filter</Button>
                <Button type="button" variant="outlined" onClick={handleClear} disabled={loading}>Clear</Button>
              </>
            )}
            {mode === 'delete' && (
              <>
                <TextField label="Employee ID" value={deleteEmpId} onChange={e => setDeleteEmpId(e.target.value)} size="small" required disabled={deleteLoading} />
                <TextField label="Date" type="date" value={deleteDate} onChange={e => setDeleteDate(e.target.value)} size="small" InputLabelProps={{ shrink: true }} disabled={deleteLoading} required />
                <Button type="button" variant="contained" color="error" onClick={handleDeleteAttendance} disabled={deleteLoading || !deleteEmpId}>Delete Attendance</Button>
                <Button type="button" variant="outlined" onClick={() => setDeleteEmpId('')} disabled={deleteLoading}>Clear</Button>
              </>
            )}
          </>
        )}
        {user && !user.is_admin && (
          <Box component="form" onSubmit={handleNonAdminFilter} display="flex" gap={2} alignItems="center" sx={{ ml: 0 }}>
            <TextField label="Employee ID or Username" value={userInput} onChange={e => setUserInput(e.target.value)} size="small" disabled={loading} required />
            <TextField label="Date" type="date" value={filterDate} onChange={handleDateChange} size="small" InputLabelProps={{ shrink: true }} disabled={loading} required />
            <Button type="submit" variant="contained" disabled={loading}>Apply Filter</Button>
            <Button type="button" variant="outlined" onClick={handleNonAdminClear} disabled={loading}>Clear</Button>
          </Box>
        )}
      </Box>

      {/* Delete confirmation dialog */}
      <Dialog open={deleteConfirmDialog.open} onClose={cancelDeleteAttendance}>
        <DialogTitle>Delete Attendance</DialogTitle>
        <DialogContent>
          <Typography>Do you want to delete attendance for employee ID: <b>{deleteConfirmDialog.empId}</b>?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={cancelDeleteAttendance} color="primary">No</Button>
          <Button onClick={confirmDeleteAttendance} color="error" disabled={deleteLoading}>Yes</Button>
        </DialogActions>
      </Dialog>

      {/* Attendance table */}
      {loading ? (
        <CircularProgress />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : Array.isArray(attendance) && attendance.length === 0 ? (
        <Alert severity="info">No attendance records found.</Alert>
      ) : (
        <>
          <AttendanceTable 
            logs={user && user.is_admin ? paginatedAttendance : attendance} 
            isAdmin={user && user.is_admin} 
            dateCol={filterDate} 
          />
          {user && user.is_admin && (
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
          )}
        </>
      )}

      {/* Notification snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={4000}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <MuiAlert
          elevation={6}
          variant="filled"
          severity={notification.severity}
          onClose={() => setNotification({ ...notification, open: false })}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </MuiAlert>
      </Snackbar>
    </Box>
  );
}