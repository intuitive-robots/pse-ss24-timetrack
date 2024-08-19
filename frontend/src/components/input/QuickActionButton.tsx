import React from 'react';

interface QuickActionButtonProps {
  label: string;
  onClick: () => void;
  textColor?: string;
  bgColor?: string;
  hover?: string;
  icon?: string;
  border?: string;
}

/**
 * ActionButton component that renders a button with specified styles and click handler.
 *
 * @component
 * @param {ActionButtonProps} props - The props passed to the ActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button with specified styles and click handler.
 */
const QuickActionButton: React.FC<QuickActionButtonProps> = ({icon, label, onClick, textColor = 'text-white', bgColor = 'bg-purple-600', hover = 'hover:bg-purple-700', border = 'none' }: QuickActionButtonProps): React.ReactElement => {
  return icon ? (
      <button
          className={`flex items-center gap-3 py-2.5 px-5 ${textColor} ${bgColor} rounded-lg shadow ${hover} transition-colors ${border}`}
          onClick={onClick}
      >
        <img src={icon} alt="" className=""/>
        <p className={`${textColor} font-semibold`}>{label}</p>
      </button>

  ) : (
      <button
          className={`flex items-center gap-3 py-2.5 px-5 ${textColor} ${bgColor} text-white rounded-lg shadow ${hover} transition-colors ${border}`}
          onClick={onClick}
      >
        <p className={`${textColor} font-semibold`}>{label}</p>
      </button>
  );
};

export default QuickActionButton;
