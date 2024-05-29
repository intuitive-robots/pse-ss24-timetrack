import React from 'react';

interface TextInputProps {
  id: string;
  label: string;
  type: string;
  value: string;
  placeholder: string;
  onChange: (value: string) => void;
}

const TextInput: React.FC<TextInputProps> = ({ id, label, type, value, placeholder, onChange }) => {
  return (
    <div className="mb-6">
      <label htmlFor={id} className="block text-start text-sm font-medium text-gray-700">{label}</label>
      <input
        type={type}
        id={id}
        placeholder={placeholder}
        value={value}
        onChange={e => onChange(e.target.value)}
        required
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
      />
    </div>
  );
};

export default TextInput;
