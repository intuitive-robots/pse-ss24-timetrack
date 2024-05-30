import React from 'react';
import {Routes, Route, Navigate} from 'react-router-dom';
import HomePage from "./pages/HomePage";
import LoginForm from "./pages/LoginPage";
import ProtectedRoute from './components/auth/ProtectedRoute';  // Ensure this is correctly imported

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/" element={
        <ProtectedRoute>
          <HomePage />
        </ProtectedRoute>
      } />
      <Route path="*" element={<Navigate replace to="/" />} />
    </Routes>
  );
}

export default App;
