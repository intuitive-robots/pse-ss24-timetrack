import React from 'react';

interface DropdownMenuButtonProps {
  icon: string;
  label: string;
  onClick: () => void;
}

const DropdownMenuButton: React.FC<DropdownMenuButtonProps> = ({ icon, label, onClick }) => {
  return (
    <button
      className="flex w-full items-center text-[#595959] text-sm font-semibold py-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-opacity-50"
      onClick={onClick}
    >
      <img src={icon} alt="icon" className="mr-2 w-5 h-5"/>
      <span>{label}</span>
    </button>
  );
};

export default DropdownMenuButton;
