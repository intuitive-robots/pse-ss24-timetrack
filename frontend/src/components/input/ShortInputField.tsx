import React from 'react';

interface ShortInputFieldProps {
  icon: string;
  type: 'text' | 'number' | 'time';
  title?: string;
  suffix?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
}

const ShortInputField: React.FC<ShortInputFieldProps> = ({
  icon,
  type,
  title,
  suffix,
  placeholder,
  value,
  onChange
}) => {
  return (
    <div className="input-container">
      {title && <h2 className="text-md font-semibold mb-1.5">{title}</h2>}
      <div className="input-wrapper flex w-fit items-center border border-gray-300 rounded-md overflow-hidden px-4 gap-1">
        <img src={icon} alt="Icon" className=""/>
        <input
          type={type}
          className="input-field flex-1 outline-none p-2"
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
        {suffix && <span className="suffix text-gray-500 p-2">{suffix}</span>}
      </div>
    </div>
  );
};


export default ShortInputField;
