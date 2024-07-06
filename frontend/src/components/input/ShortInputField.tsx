import React from 'react';

interface ShortInputFieldProps {
  icon: string;
  type: 'text' | 'number' | 'time';
  title?: string;
  suffix?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  size?: string;
}

const ShortInputField: React.FC<ShortInputFieldProps> = ({
  icon,
  type,
  title,
  suffix,
  placeholder,
  value,
  onChange, size
}) => {
  const getWidthClass = (size: string | undefined) => {
    if (!size) return 'w-fit';
    switch (size) {
      case 'small': return 'w-44';
      case 'medium': return 'w-56';
      case 'large': return 'w-96';
      default: return 'w-fit';
    }
  };

  return (
    <div className="input-container">
      {title && <h2 className="text-md font-semibold mb-1.5">{title}</h2>}
      <div className={`input-wrapper flex items-center border border-gray-300 rounded-md overflow-hidden px-4 gap-1 ${getWidthClass(size)}`}>
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
