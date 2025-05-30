import React, { createContext, useContext, useRef } from 'react';

// Context to notify when a user is updated anywhere in the app
export const UserUpdateContext = createContext({ notifyUserUpdated: () => {}, subscribe: () => {} });

export function UserUpdateProvider({ children }) {
  // Subscribers are callback functions
  const subscribersRef = useRef([]);

  const notifyUserUpdated = () => {
    subscribersRef.current.forEach(cb => cb());
  };

  const subscribe = (cb) => {
    subscribersRef.current.push(cb);
    return () => {
      subscribersRef.current = subscribersRef.current.filter(fn => fn !== cb);
    };
  };

  return (
    <UserUpdateContext.Provider value={{ notifyUserUpdated, subscribe }}>
      {children}
    </UserUpdateContext.Provider>
  );
}

export function useUserUpdate() {
  return useContext(UserUpdateContext);
}
