import React, {ReactNode} from 'react';
import { usePopup } from '../popup/PopupContext';
import ActionButton from './ActionButton';

interface PopupActionButtonProps {
  label: string;
  popupComponent: ReactNode;
  bgColor?: string;
  hover?: string;
  icon: string;
  primary?: boolean;
  secondary?: boolean;
}

/**
 * PopupActionButton component that renders a button which opens a popup on click.
 *
 * @component
 * @param {PopupActionButtonProps} props - The props passed to the PopupActionButton component.
 * @returns {React.ReactElement} A React Element that renders a button which, when clicked, displays a popup.
 */
const PopupActionButton: React.FC<PopupActionButtonProps> = ({
  icon,
  label,
  popupComponent,
  bgColor,
  hover,
  primary = false,
  secondary = false
}: PopupActionButtonProps): React.ReactElement => {
  const { openPopup } = usePopup();

  const handleOpenPopup = () => {
    openPopup(popupComponent);
  };

  return (
    <ActionButton
      icon={icon}
      label={label}
      onClick={handleOpenPopup}
      bgColor={bgColor}
      hover={hover}
      primary={primary}
      secondary={secondary}
    />
  );
};

export default PopupActionButton;
