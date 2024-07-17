import React, {createContext, useContext, useState, ReactNode, useCallback} from 'react';

interface PopupContextType {
  popupContent: ReactNode;
  openPopup: (content: ReactNode, onCloseComplete?: () => void) => void;
  closePopup: () => void;
}

const initialPopupState: PopupContextType = {
  popupContent: null,
  openPopup: () => {},
  closePopup: () => {}
};

const PopupContext = createContext<PopupContextType>(initialPopupState);

export const usePopup = () => useContext(PopupContext);

export const PopupProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [popupContent, setPopupContent] = useState<ReactNode>(null);
  const [onCloseComplete, setOnCloseComplete] = useState<() => void | undefined>();

  const openPopup = useCallback((content: ReactNode, onCloseComplete?: () => void) => {
    setPopupContent(content);
    setOnCloseComplete(() => onCloseComplete);
  }, []);

  const closePopup = useCallback(() => {
    setPopupContent(null);
    if (onCloseComplete) {
      onCloseComplete();
      setOnCloseComplete(undefined);
    }
  }, [onCloseComplete]);

  return (
    <PopupContext.Provider value={{ popupContent, openPopup, closePopup }}>
      {children}
    </PopupContext.Provider>
  );
};
