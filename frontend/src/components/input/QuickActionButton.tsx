import React from 'react';

interface QuickActionButtonProps {
  label: string;
  onClick: () => void;
  bgColor: string;
  hover: string;
  icon: string;
}

/**
 * ActionButton component that renders a button with specified styles and click handler.
 *
 * @component
 * @param {ActionButtonProps} props - The props passed to the ActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button with specified styles and click handler.
 */
const QuickActionButton: React.FC<QuickActionButtonProps> = ({icon, label, onClick, bgColor, hover }: QuickActionButtonProps): React.ReactElement => {
  return (
    <button
      className={`flex items-center gap-3 py-2.5 px-5 ${bgColor} text-white rounded-lg shadow mt-4 ${hover} transition-colors`}
      onClick={onClick}
    >
      <img src={icon} alt="" className=""/>
      <p className="text-white font-semibold">{label}</p>
    </button>
  );
};

export default QuickActionButton;
