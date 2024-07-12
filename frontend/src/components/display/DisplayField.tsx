import React from 'react';

interface DisplayFieldProps {
  label: string;
  value: string;
  icon: string;
}

const DisplayField: React.FC<DisplayFieldProps> = ({ label, value, icon }) => {
  return (
    <div className="input-container">
      <h2 className="text-md font-semibold mb-1.5">{label}</h2>
      <div className="input-wrapper flex items-center border border-gray-300 rounded-md overflow-hidden px-4 gap-1 w-56">
        <img src={icon} alt="Icon" className="h-5 w-5"/>
        <div className="input-field flex-1 outline-none p-2 text-gray-700">{value}</div>
      </div>
    </div>
  );
};

export default DisplayField;
