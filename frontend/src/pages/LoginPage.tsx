import React, { useState } from 'react';
import TextInput from '../components/input/TextInput';
import {login} from "../services/AuthService";

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await login(username, password);  // Use the login function from AuthService
      console.log('Login Success:', response);
    } catch (error) {
      console.error('Login Error:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white px-8 py-8 rounded-xl shadow-profilebar-shadow">
        <h2 className="text-2xl font-bold mb-3 text-start">Sign In</h2>
        <p className="mb-6 text-md font-medium text-gray-500 text-center">Nice to meet you! Enter your details to
          login.</p>
        <TextInput
            id="username"
            label="Username"
            type="text"
            value={username}
            placeholder="name@example.com"
            onChange={setUsername}
        />
        <TextInput
            id="password"
            label="Password"
            type="password"
            value={password}
            placeholder="Enter your password"
            onChange={setPassword}
        />
        <button type="submit"
                className="w-full bg-gray-950 text-white font-bold py-3 px-4 rounded-lg hover:bg-gray-700">
          LOGIN
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
