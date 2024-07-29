import React from 'react';

interface DropdownProps {
    title: string;
    value: string;
    onChange: (value: string) => void;
    options: { label: string; value: string }[];
    icon: string | React.ReactNode;
    width?: string;
}

const Dropdown: React.FC<DropdownProps> = ({ title, value, onChange, options, icon, width = "w-full" }) => {
    return (
        <div className={`flex flex-col mb-4 ${width}`}>
            <label className="font-semibold mb-2">{title}</label>
            <div className="relative">
                <select
                    className="appearance-none w-full bg-white border border-gray-300 rounded-md py-2.5 pl-10 pr-4 leading-tight focus:outline-none focus:ring-1 focus:ring-purple-500 focus:border-transparent"
                    value={value}
                    onChange={e => onChange(e.target.value)}
                >
                    {options.map(option => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    {typeof icon === 'string' ? (
                        <img src={icon} alt="" className="h-5 w-5 text-gray-500" />
                    ) : (
                        icon
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dropdown;

