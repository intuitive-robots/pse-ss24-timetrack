import React, {ReactNode} from 'react';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  textColor?: string;
  bgColor?: string;
  hover?: string;
  border?: string;
  icon?: string | ReactNode;
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
  onClick, textColor = 'text-white', bgColor, hover, border = 'none',
  primary = false,
  secondary = false
}: ActionButtonProps): React.ReactElement => {
  const primaryClass = "bg-purple-600 hover:bg-purple-700";
  const secondaryClass = "bg-[#20192E] hover:bg-gray-800";
  const defaultClass = "";

  const buttonClass = primary ? primaryClass : secondary ? secondaryClass : defaultClass;

  const iconElement = typeof icon === 'string' ? (
    <img src={icon} alt="" className=""/>
  ) : (
    icon
  );

  return icon ? (
      <button
          className={`flex items-center gap-3 w-full py-3 px-5 ${buttonClass} ${bgColor} ${textColor} rounded-md shadow mt-4 ${hover} transition-colors ${border}`}
          onClick={onClick}
      >
        {iconElement}
        <p className={`${textColor} font-semibold text-nowrap`}>{label}</p>
      </button>

  ) : (
      <button
          className={`flex items-center gap-3 py-3 px-5 ${buttonClass} ${bgColor} ${textColor} rounded-md shadow mt-4 ${hover} transition-colors ${border}`}
          onClick={onClick}
      >
        <p className={`${textColor} font-semibold text-nowrap`}>{label}</p>
      </button>
  );
};


export default ActionButton;
