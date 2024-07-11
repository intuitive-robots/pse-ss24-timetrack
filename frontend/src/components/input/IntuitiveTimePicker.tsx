import React from 'react';
import TimeIcon from "../../assets/images/time_icon.svg";

interface IntuitiveTimePickerProps {
  placeholder?: string;
  value: string; // This should be in "HH:mm" format
  onChange: (value: string) => void;
}

const IntuitiveTimePicker: React.FC<IntuitiveTimePickerProps> = ({ placeholder, value, onChange }) => {
  return (
      <div className="flex items-center relative border border-gray-300 rounded-md shadow-sm w-36">
          <img src={TimeIcon} alt="Time Icon" className="absolute left-3"/>
          <input
              type="time"
              className="input-field flex-1 outline-none pl-11 p-2 rounded-md font-medium text-[#6B6B6B] focus:border-purple-500 focus:ring focus:ring-purple-500 focus:ring-opacity-50"
              placeholder={placeholder}
              value={value}
              onChange={(e) => onChange(e.target.value)}
          />
      </div>
  );
};

export default IntuitiveTimePicker;
