import React, { useState, useRef, useEffect } from 'react';
import { Box, IconButton, TextField, Typography, Paper, List, ListItem, ListItemText, Collapse, Fade, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';
import { sendMessage, getTodayAttendance, getAttendanceByDate } from '../api/chatbot';

const Chatbot = () => {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! I am your attendance assistant. How can I help you?', options: ['Hi'] },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [confirmClearOpen, setConfirmClearOpen] = useState(false);
  const [awaitingDateInput, setAwaitingDateInput] = useState(false);
  const [currentEmpId, setCurrentEmpId] = useState(null); // eslint-disable-line no-unused-vars
  const messagesEndRef = useRef(null);

  const toggleOpen = () => {
    setOpen(!open);
  };

  const handleClearClick = () => {
    setConfirmClearOpen(true);
  };

  const handleClearConfirm = () => {
    setMessages([{ sender: 'bot', text: 'Hi! I am your attendance assistant. How can I help you?', options: ['Hi'] }]);
    setConfirmClearOpen(false);
  };

  const handleClearCancel = () => {
    setConfirmClearOpen(false);
  };

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const response = await sendMessage("who am i?");
        const empIdMatch = response.response.match(/employee ID (\w+)/i);
        if (empIdMatch && empIdMatch[1]) {
          setCurrentEmpId(empIdMatch[1]);
        }
      } catch (error) {
        console.error("Failed to fetch current user emp_id:", error);
      }
    };
    fetchCurrentUser();
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    if (awaitingDateInput) {
      // User entered a date for attendance query
      const dateStr = input.trim();
      const userMessage = { sender: 'user', text: dateStr };
      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      setLoading(true);
      setAwaitingDateInput(false);
      try {
        const attendanceArray = await getAttendanceByDate(dateStr);
        const currentUserAttendance = attendanceArray.find(record => record.emp_id === currentEmpId) || null;
        // Override date with the input dateStr
        if (currentUserAttendance) {
          currentUserAttendance.date = dateStr;
        }
        const attendanceText = formatAttendance(currentUserAttendance);
        const defaultOptions = ['Hi', 'Who am i?', 'attendance','Back'];
        const botMessage = { sender: 'bot', text: attendanceText, options: defaultOptions };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = { sender: 'bot', text: 'Failed to fetch attendance for the date. Please ensure the date is in YYYY-MM-DD format.', options: [] };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
      return;
    }

    const userMessage = { sender: 'user', text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    try {
      const response = await sendMessage(userMessage.text);
      const botMessage = { sender: 'bot', text: response.response, options: response.options || [] };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { sender: 'bot', text: 'Sorry, there was an error. Please try again later.', options: [] };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !loading) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleOptionClick = async (option) => {
    if (option === "Show attendance for today") {
      setLoading(true);
      const userMessage = { sender: 'user', text: option };
      setMessages((prev) => [...prev, userMessage]);
      try {
        const attendanceArray = await getTodayAttendance();
        const currentUserAttendance = attendanceArray.find(record => record.emp_id === currentEmpId) || null;
        const attendanceText = formatAttendance(currentUserAttendance);
        const defaultOptions = ['Hi', 'Who am i?' ,'attendance', 'Show attendance for today', 'Show attendance for a particular day', 'Back'];
        const botMessage = { sender: 'bot', text: attendanceText, options: defaultOptions };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = { sender: 'bot', text: 'Failed to fetch today\'s attendance.', options: [] };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    } else if (option === "Show attendance for a particular day") {
      const userMessage = { sender: 'user', text: option };
      setMessages((prev) => [...prev, userMessage]);
      setAwaitingDateInput(true);
      const botMessage = { sender: 'bot', text: 'Please enter the date in YYYY-MM-DD format.', options: [] };
      setMessages((prev) => [...prev, botMessage]);
    } else if (option === "Back") {
      // Provide default options and greeting on back
      const botMessage = { sender: 'bot', text: 'Hi! I am your attendance assistant. How can I help you?', options: ['Hi','Who am i?' ,'attendance','Show attendance for today', 'Show attendance for a particular day'] };
      setMessages((prev) => [...prev, botMessage]);
    } else {
      // Default behavior for other options
      const userMessage = { sender: 'user', text: option };
      setMessages((prev) => [...prev, userMessage]);
      setLoading(true);
      setInput('');
      try {
        const response = await sendMessage(option);
        const botMessage = { sender: 'bot', text: response.response, options: response.options || [] };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = { sender: 'bot', text: 'Sorry, there was an error. Please try again later.', options: [] };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    }
  };

  const formatAttendance = (attendance) => {
    if (!attendance || attendance.message) {
      return attendance.message || 'No attendance data available.';
    }
    const empId = attendance.emp_id || 'N/A';
    // Extract date from first_in or last_out if date is missing or N/A
    let date = attendance.date;
    if (!date || date === 'N/A') {
      if (attendance.first_in) {
        date = attendance.first_in.split(' ')[0];
      } else if (attendance.last_out) {
        date = attendance.last_out.split(' ')[0];
      } else {
        date = new Date().toISOString().split('T')[0];
      }
    }
    const inTime = attendance.first_in || 'N/A';
    const outTime = attendance.last_out || 'N/A';
    return `Employee ID: ${empId}\nDate: ${date}\nIn Time: ${inTime}\nOut Time: ${outTime}`;
  };

  return (
    <>
      <Box sx={{ position: 'absolute', top: 96, right: 16, zIndex: 1300, display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
        <Typography variant="subtitle2" sx={{ mb: 1, color: 'text.secondary', fontWeight: 'bold' }}>Attendance Chatbot</Typography>
        {!open && (
          <Fade in={!open}>
            <IconButton color="primary" onClick={toggleOpen} aria-label="Open chat" sx={{ boxShadow: 3 }}>
              <ChatIcon fontSize="large" />
            </IconButton>
          </Fade>
        )}
        <Collapse in={open}>
          <Paper elevation={6} sx={{ width: 320, height: 440, display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 1, bgcolor: 'primary.main', color: 'primary.contrastText', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">Attendance Chatbot</Typography>
              <IconButton color="inherit" onClick={toggleOpen} aria-label="Close chat">
                <CloseIcon />
              </IconButton>
            </Box>
            <List sx={{ flexGrow: 1, overflowY: 'auto', p: 1, position: 'relative' }}>
              {messages.map((msg, index) => (
                <ListItem key={index} sx={{ flexDirection: 'column', alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start' }}>
                  <ListItemText
                    primary={msg.text}
                    sx={{
                      bgcolor: msg.sender === 'user' ? 'primary.light' : 'grey.300',
                      borderRadius: 2,
                      px: 2,
                      py: 1,
                      maxWidth: '75%',
                      wordBreak: 'break-word',
                    }}
                  />
                  {msg.options && msg.options.length > 0 && (
                    <Box sx={{ mt: 1, display: 'flex', flexDirection: 'column', gap: 1 }}>
                      {msg.options.map((option, i) => (
                        <Button
                          key={i}
                          variant="outlined"
                          size="small"
                          onClick={() => handleOptionClick(option)}
                        >
                          {option}
                        </Button>
                      ))}
                    </Box>
                  )}
                </ListItem>
              ))}
              <div ref={messagesEndRef} />
            </List>
            <Box sx={{ p: 1, display: 'flex', justifyContent: 'center' }}>
              <Button variant="outlined" color="primary" onClick={handleClearClick} sx={{ fontWeight: 'bold' }}>
                Clear Chat
              </Button>
            </Box>
            <Box sx={{ p: 1, display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                size="small"
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
              />
              <IconButton color="primary" onClick={handleSend} disabled={loading} aria-label="Send message">
                <ChatIcon />
              </IconButton>
            </Box>
          </Paper>
        </Collapse>
      </Box>
      <Dialog
        open={confirmClearOpen}
        onClose={handleClearCancel}
        aria-labelledby="confirm-clear-dialog-title"
        aria-describedby="confirm-clear-dialog-description"
      >
        <DialogTitle id="confirm-clear-dialog-title">Clear Chat</DialogTitle>
        <DialogContent>
          <DialogContentText id="confirm-clear-dialog-description">
            Are you sure you want to clear the chat history? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClearCancel} color="primary">
            Cancel
          </Button>
          <Button onClick={handleClearConfirm} color="primary" autoFocus>
            Clear
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default Chatbot;
