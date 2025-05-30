import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import { format, parseISO } from 'date-fns';

export default function AttendanceTable({ logs, isAdmin, dateCol }) {
  if (!logs || logs.length === 0) {
    return <Typography>No attendance records found.</Typography>;
  }
  // Helper to get day of week
  const getDay = (dateStr) => {
    if (!dateStr) return '-';
    try {
      const date = dateStr.length > 10 ? parseISO(dateStr.split(' ')[0]) : parseISO(dateStr);
      return format(date, 'EEE');
    } catch {
      return '-';
    }
  };
  // If admin and logs is an array of users, show all users
  if (isAdmin && Array.isArray(logs)) {
    return (
      <TableContainer component={Paper} sx={{ mt: 2, borderRadius: 3, boxShadow: 6, border: '1px solid #e0e0e0', background: theme => theme.palette.mode === 'dark' ? '#23272f' : '#f8fafc' }}>
        <Table sx={{ minWidth: 700 }}>
          <TableHead>
            <TableRow sx={{ background: theme => theme.palette.mode === 'dark' ? '#18181b' : '#ede9fe' }}>
              <TableCell>Date</TableCell>
              <TableCell>Day</TableCell>
              <TableCell>Employee ID</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>Sub-Department</TableCell>
              <TableCell>In Time</TableCell>
              <TableCell>Out Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.map((row, idx) => (
              <TableRow key={idx}>
                <TableCell>{row.first_in ? row.first_in.split(' ')[0] : (dateCol || '-')}</TableCell>
                <TableCell>{getDay(row.first_in ? row.first_in.split(' ')[0] : dateCol)}</TableCell>
                <TableCell>{row.emp_id || '-'}</TableCell>
                <TableCell>{row.username || '-'}</TableCell>
                <TableCell>{row.department || '-'}</TableCell>
                <TableCell>{row.sub_department || '-'}</TableCell>
                <TableCell>{row.username === 'root' ? 'No data' : (row.first_in || '-')}</TableCell>
                <TableCell>{row.username === 'root' ? 'No data' : (row.last_out || '-')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  // Single user (filtered by emp_id and date)
  if (isAdmin && logs && (logs.emp_id || logs.employee_id)) {
    const row = Array.isArray(logs) ? logs[0] : logs;
    return (
      <TableContainer component={Paper} sx={{ mt: 2, borderRadius: 3, boxShadow: 6, border: '1px solid #e0e0e0', background: theme => theme.palette.mode === 'dark' ? '#23272f' : '#f8fafc' }}>
        <Table sx={{ minWidth: 700 }}>
          <TableHead>
            <TableRow sx={{ background: theme => theme.palette.mode === 'dark' ? '#18181b' : '#ede9fe' }}>
              <TableCell>Date</TableCell>
              <TableCell>Day</TableCell>
              <TableCell>Employee ID</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>Sub-Department</TableCell>
              <TableCell>In Time</TableCell>
              <TableCell>Out Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{row.first_in ? row.first_in.split(' ')[0] : (dateCol || '-')}</TableCell>
              <TableCell>{getDay(row.first_in ? row.first_in.split(' ')[0] : dateCol)}</TableCell>
              <TableCell>{row.emp_id || '-'}</TableCell>
              <TableCell>{row.username || row.name || '-'}</TableCell>
              <TableCell>{row.department || (row.user && row.user.department) || '-'}</TableCell>
              <TableCell>{row.sub_department || (row.user && row.user.sub_department) || '-'}</TableCell>
              <TableCell>{row.username === 'root' ? 'No data' : (row.first_in || '-')}</TableCell>
              <TableCell>{row.username === 'root' ? 'No data' : (row.last_out || '-')}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  // Single user (non-admin or filtered)
  const row = Array.isArray(logs) ? logs[0] : logs;
  return (
    <TableContainer component={Paper} sx={{ mt: 2, borderRadius: 3, boxShadow: 6, border: '1px solid #e0e0e0', background: theme => theme.palette.mode === 'dark' ? '#23272f' : '#f8fafc' }}>
      <Table sx={{ minWidth: 700 }}>
        <TableHead>
          <TableRow sx={{ background: theme => theme.palette.mode === 'dark' ? '#18181b' : '#ede9fe' }}>
            <TableCell>Date</TableCell>
            <TableCell>Day</TableCell>
            <TableCell>Employee ID</TableCell>
            <TableCell>Username</TableCell>
            <TableCell>Department</TableCell>
            <TableCell>Sub-Department</TableCell>
            <TableCell>In Time</TableCell>
            <TableCell>Out Time</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>{row.first_in ? row.first_in.split(' ')[0] : (dateCol || '-')}</TableCell>
            <TableCell>{getDay(row.first_in ? row.first_in.split(' ')[0] : dateCol)}</TableCell>
            <TableCell>{row.emp_id || '-'}</TableCell>
            <TableCell>{row.username || row.name || '-'}</TableCell>
            <TableCell>{row.department || (row.user && row.user.department) || '-'}</TableCell>
            <TableCell>{row.sub_department || (row.user && row.user.sub_department) || '-'}</TableCell>
            <TableCell>{row.username === 'root' ? 'No data' : (row.first_in || '-')}</TableCell>
            <TableCell>{row.username === 'root' ? 'No data' : (row.last_out || '-')}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}
