import React, {useState} from 'react';

interface ShortInputFieldProps {
  icon: string | React.ReactNode;
  type: 'text' | 'number' | 'time';
  title?: string;
  suffix?: string;
  placeholder?: string;
  value: string | number;
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
  const [isFocused, setIsFocused] = useState(false);

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
      <div className={`input-wrapper flex items-center border ${isFocused ? 'border-purple-500' : 'border-gray-300'} rounded-md overflow-hidden px-4 gap-1 ${getWidthClass(size)}`}>
         {typeof icon === 'string' ? (
          <img src={icon} alt="Icon" className=""/>
        ) : (
          <span className="icon-component">{icon}</span>
        )}
        <input
          type={type}
          className="input-field flex-1 outline-none p-2"
          placeholder={placeholder}
          value={value}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onChange={(e) => onChange(e.target.value)}
        />
        {suffix && <span className="suffix text-gray-500 p-2">{suffix}</span>}
      </div>
    </div>
  );
};


export default ShortInputField;
