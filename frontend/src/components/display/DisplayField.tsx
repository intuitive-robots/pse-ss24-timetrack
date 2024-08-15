import React from 'react';
import { ReactNode } from 'react';

interface DisplayFieldProps {
  label: string;
  value: string;
  icon: ReactNode;
}

const DisplayField: React.FC<DisplayFieldProps> = ({ label, value, icon }) => {
  return (
    <div className="input-container">
      <h2 className="text-md font-semibold text-[#494949] mb-1.5">{label}</h2>
      <div className="input-wrapper flex items-center border border-gray-300 rounded-md overflow-hidden px-4 gap-1 w-56">
        <div className="flex-shrink-0">
          {icon}
        </div>
        <div className="input-field flex-1 outline-none p-2 text-[#494949] truncate">
          {value}
        </div>
      </div>
    </div>
  );
};

export default DisplayField;
