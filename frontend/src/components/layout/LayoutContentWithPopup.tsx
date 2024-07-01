import React, {FC, ReactNode} from 'react';
import { Routes, Route } from 'react-router-dom';
import {usePopup} from "../popup/PopupContext";

interface ContentWithPopupProps {
  currentRoutes: Record<string, React.ComponentType<any>>;
}

const LayoutContentWithPopup: FC<ContentWithPopupProps> = ({ currentRoutes }) => {
  const { popupContent } = usePopup();

  return (
    <>
      <div className={`flex-1 overflow-auto p-4 ${popupContent ? "opacity-50" : ""}`}>
        <Routes>
          {Object.entries(currentRoutes).map(([path, Component]) => (
            <Route key={path} path={path} element={<Component />} />
          ))}
        </Routes>
      </div>
      {popupContent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-5 rounded-lg">
            {popupContent}
          </div>
        </div>
      )}
    </>
  );
};

export default LayoutContentWithPopup;
