import React from 'react';

interface RequireAuthProps {
  children: React.ReactNode;
}

export default function RequireAuth({ children }: RequireAuthProps) {
  // Login removed for the static demo build — the app runs entirely on mock data,
  // so every route is open and lands straight on the dashboard.
  return <>{children}</>;
}
