import React, {useState} from 'react';
import TextInput from '../components/input/TextInput';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {EyeFilledIcon} from "../assets/iconComponents/EyeFilledIcon";
import {EyeNotFilledIcon} from "../assets/iconComponents/EyeNotFilledIcon";

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const { login, isAuthenticated} = useAuth();

  if (isAuthenticated) {
    navigate('/');
  }

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      await login(username, password);
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
            placeholder="Enter your username"
            onChange={setUsername}
        />
        <div className="relative">
          <TextInput
              id="password"
              label="Password"
              type={showPassword ? "text" : "password"}
              value={password}
              placeholder="Enter your password"
              onChange={setPassword}
          />
          <div className="absolute inset-y-0 top-7 right-2 flex items-center pr-3 cursor-pointer"
               onClick={togglePasswordVisibility}>
            {showPassword ? <EyeFilledIcon className="hover:fill-gray-600 fill-gray-800"/> : <EyeNotFilledIcon className="hover:fill-gray-600 fill-gray-800"/>}
          </div>
        </div>
        <button type="submit"
                className="w-full bg-gray-950 text-white font-bold py-3 px-4 rounded-lg hover:bg-gray-700">
          LOGIN
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
