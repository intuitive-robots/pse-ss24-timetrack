import React, {useState} from 'react';
import TimeIcon from "../../assets/images/time_icon.svg";

interface IntuitiveTimePickerProps {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
}

const IntuitiveTimePicker: React.FC<IntuitiveTimePickerProps> = ({ placeholder, value, onChange }) => {
    const [isFocused, setIsFocused] = useState(false);

    return (
      <div className="flex items-center relative  rounded-md shadow-sm w-36">
          <img src={TimeIcon} alt="Time Icon" className="absolute left-3"/>
          <input
              type="time"
              className="input-field flex-1 outline-none pl-11 p-2 rounded-md font-medium text-[#6B6B6B] border border-gray-300 focus:border-purple-500"
              placeholder={placeholder}
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
          />
      </div>
    );
};

export default IntuitiveTimePicker;
