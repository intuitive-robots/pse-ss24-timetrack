import React from 'react';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  bgColor: string;
  hoverBgColor: string;
  icon: string;
}

/**
 * ActionButton component that renders a button with specified styles and click handler.
 *
 * @component
 * @param {ActionButtonProps} props - The props passed to the ActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button with specified styles and click handler.
 */
const ActionButton: React.FC<ActionButtonProps> = ({icon, label, onClick, bgColor, hoverBgColor }: ActionButtonProps): React.ReactElement => {
  return (
    <button
      className={`flex items-center gap-3 w-full py-3 px-5 ${bgColor} text-white rounded-md shadow mt-4 hover:${hoverBgColor} transition-colors`}
      onClick={onClick}
    >
      <img src={icon} alt="" className=""/>
      <p className="text-white font-semibold">{label}</p>
    </button>
  );
};

export default ActionButton;
