import React from 'react';
import {Routes, Route, Navigate} from 'react-router-dom';
import LoginForm from "./pages/LoginPage";
import ProtectedRoute from './components/auth/ProtectedRoute';
import LayoutWrapper from "./components/LayoutWrapper";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/app/*" element={
        <ProtectedRoute>
          <LayoutWrapper pageContent={<div/>}/>
        </ProtectedRoute>
      } />
      <Route path="*" element={<Navigate replace to="/app/home" />} />
    </Routes>
  );
}

export default App;
