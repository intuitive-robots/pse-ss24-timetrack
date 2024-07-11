import React, {FC} from 'react';
import { Routes, Route } from 'react-router-dom';
import {usePopup} from "../popup/PopupContext";

interface ContentWithPopupProps {
  currentRoutes: Record<string, React.ComponentType<any>>;
}

const LayoutContentWithPopup: FC<ContentWithPopupProps> = ({ currentRoutes }) => {
  const { popupContent } = usePopup();

  return (
    <>
      <div className={`h-full w-full  ${popupContent ? "opacity-50" : ""}`}>
        <Routes>
          {Object.entries(currentRoutes).map(([path, Component]) => (
            <Route key={path} path={path} element={<Component />} />
          ))}
        </Routes>
      </div>
      {popupContent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white px-7 py-5 rounded-xl">
            {popupContent}
          </div>
        </div>
      )}
    </>
  );
};

export default LayoutContentWithPopup;
