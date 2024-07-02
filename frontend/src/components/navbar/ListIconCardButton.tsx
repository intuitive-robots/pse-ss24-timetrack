import React from 'react';

interface ListIconCardButtonProps {
  iconSrc: string;
  label: string;
  onClick: () => void;
}

/**
 * ListIconCardButton component renders a button with an SVG icon and label.
 *
 * @component
 * @param {ListIconCardButtonProps} props - The props passed to the ListIconCardButton component.
 * @returns {React.ReactElement} A React Element that renders a button with an SVG icon and label.
 */
const ListIconCardButton: React.FC<ListIconCardButtonProps> = ({ iconSrc, label, onClick }) => {
  return (
    <button
      className="flex items-center px-4 py-2 border rounded-lg text-gray-500 hover:bg-gray-100"
      onClick={onClick}
    >
      <img src={iconSrc} alt={label} className="h-5 w-5 mr-2" />
      <p className="font-semibold text-[#717171]">{label}</p>
    </button>
  );
};

export default ListIconCardButton;
