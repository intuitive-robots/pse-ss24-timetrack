import React from 'react';

interface DropdownProps {
    title: string;
    value: string;
    onChange: (value: string) => void;
    options: string[];
    icon: string;
}

const Dropdown: React.FC<DropdownProps> = ({ title, value, onChange, options, icon }) => {
    return (
        <div className="flex flex-col mb-4 w-40">
            <label className="font-semibold mb-2">{title}</label>
            <div className="relative">
                <select
                    className="appearance-none w-full bg-white border border-gray-300 rounded-md py-2.5 pl-10 pr-4 leading-tight focus:outline-none focus:ring-1 focus:ring-purple-500 focus:border-transparent"
                    value={value}
                    onChange={e => onChange(e.target.value)}
                >
                    {options.map(option => (
                        <option key={option} value={option}>
                            {option}
                        </option>
                    ))}
                </select>
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <img src={icon} alt="" className="h-5 w-5 text-gray-500"/>
                </div>
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd"
                              d="M5.29279 7.29259C5.48031 7.10512 5.73462 6.99981 5.99979 6.99981C6.26495 6.99981 6.51926 7.10512 6.70679 7.29259L9.99979 10.5856L13.2928 7.29259C13.385 7.19708 13.4954 7.1209 13.6174 7.06849C13.7394 7.01608 13.8706 6.9885 14.0034 6.98734C14.1362 6.98619 14.2678 7.01149 14.3907 7.06177C14.5136 7.11205 14.6253 7.18631 14.7192 7.2802C14.8131 7.37409 14.8873 7.48574 14.9376 7.60864C14.9879 7.73154 15.0132 7.86321 15.012 7.99599C15.0109 8.12877 14.9833 8.25999 14.9309 8.382C14.8785 8.504 14.8023 8.61435 14.7068 8.70659L10.7068 12.7066C10.5193 12.8941 10.265 12.9994 9.99979 12.9994C9.73462 12.9994 9.48031 12.8941 9.29279 12.7066L5.29279 8.70659C5.10532 8.51907 5 8.26476 5 7.99959C5 7.73443 5.10532 7.48012 5.29279 7.29259Z"
                              fill="#6B6B6B"/>
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default Dropdown;
