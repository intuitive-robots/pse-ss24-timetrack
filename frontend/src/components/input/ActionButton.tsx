import React from 'react';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  bgColor?: string;
  hover?: string;
  icon: string;
  primary?: boolean;
  secondary?: boolean;
}

/**
 * ActionButton component that renders a button with specified styles and click handler.
 *
 * @component
 * @param {ActionButtonProps} props - The props passed to the ActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button with specified styles and click handler.
 */
const ActionButton: React.FC<ActionButtonProps> = ({
  icon,
  label,
  onClick, bgColor, hover,
  primary = false,
  secondary = false
}: ActionButtonProps): React.ReactElement => {
  const primaryClass = "bg-purple-600 hover:bg-purple-700";
  const secondaryClass = "bg-[#20192E] hover:bg-gray-800";
  const defaultClass = "";

  const buttonClass = primary ? primaryClass : secondary ? secondaryClass : defaultClass;

  return (
    <button
      className={`flex items-center gap-3 w-full py-3 px-5 ${buttonClass} ${bgColor} text-white rounded-md shadow mt-4 ${hover} transition-colors`}
      onClick={onClick}
    >
      <img src={icon} alt="" className=""/>
      <p className="text-white font-semibold">{label}</p>
    </button>
  );
};

export default ActionButton;
