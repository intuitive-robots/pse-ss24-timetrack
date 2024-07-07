import React, {ReactNode} from 'react';
import { usePopup } from '../popup/PopupContext';
import ActionButton from './ActionButton';

interface PopupActionButtonProps {
  label: string;
  popupComponent: ReactNode;
  textColor?: string;
  bgColor?: string;
  hover?: string;
  icon?: string;
  border?: string;
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
  popupComponent, textColor,
  bgColor,
  hover, border = 'none',
  primary = false,
  secondary = false
}: PopupActionButtonProps): React.ReactElement => {
  const { openPopup } = usePopup();

  const handleOpenPopup = () => {
    openPopup(popupComponent);
  };

  return icon ? (
      <ActionButton
      icon={icon}
      label={label}
      onClick={handleOpenPopup}
      textColor={textColor}
      bgColor={bgColor}
      hover={hover}
      border={border}
      primary={primary}
      secondary={secondary}
    />

  ) : (
      <ActionButton
      label={label}
      onClick={handleOpenPopup}
      textColor={textColor}
      bgColor={bgColor}
      hover={hover}
      border={border}
      primary={primary}
      secondary={secondary}
    />
  );
};


export default PopupActionButton;
