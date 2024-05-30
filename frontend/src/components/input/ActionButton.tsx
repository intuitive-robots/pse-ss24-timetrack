import React from 'react';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  bgColor: string;
  hoverBgColor: string;
}

/**
 * ActionButton component that renders a button with specified styles and click handler.
 *
 * @component
 * @param {ActionButtonProps} props - The props passed to the ActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button with specified styles and click handler.
 */
const ActionButton: React.FC<ActionButtonProps> = ({ label, onClick, bgColor, hoverBgColor }: ActionButtonProps): React.ReactElement => {
  return (
    <button
      className={`w-full py-2.5 px-4 ${bgColor} text-white rounded-md shadow mt-4 hover:${hoverBgColor} transition-colors`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default ActionButton;
