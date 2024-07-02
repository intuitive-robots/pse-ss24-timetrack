import React, { createContext, useContext, useState, ReactNode } from 'react';

interface PopupContextType {
  popupContent: ReactNode;
  openPopup: (content: ReactNode) => void;
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

  const openPopup = (content: ReactNode) => setPopupContent(content);
  const closePopup = () => setPopupContent(null);

  return (
    <PopupContext.Provider value={{ popupContent, openPopup, closePopup }}>
      {children}
    </PopupContext.Provider>
  );
};
