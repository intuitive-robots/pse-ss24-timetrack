import React from 'react';

interface DialogButtonProps {
  label: string;
  primary?: boolean;
  secondary?: boolean;
  onClick: () => void;
}

const DialogButton: React.FC<DialogButtonProps> = ({
  label,
  primary = false,
  secondary = false,
  onClick,
}) => {
  // Bestimme die CSS-Klassen basierend auf den Props
  const buttonClass = primary
    ? "bg-purple-600 hover:bg-purple-700 text-white"
    : secondary
    ? "border hover:bg-purple-200 text-purple-600 border-purple-600"
    : "bg-gray-200 hover:bg-gray-300 text-gray-800";
  return (
    <button
      className={`transition ease-in duration-100 rounded-xl py-1.5 px-7 font-medium ${buttonClass}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default DialogButton;
