import React from 'react';
import NavigationBar from './navbar/NavigationBar';
import {Routes, Route } from 'react-router-dom';
import ProfileBar from './profile/ProfileBar';
import HomePage from "../pages/home-page/HomePage";
import GuidelinePage from "../pages/GuidelinePage";

interface LayoutWrapperProps {
  pageContent: React.ReactNode;
}

/**
 * The LayoutWrapper component is responsible for providing the overall page layout.
 * It includes a profile bar at the top, a navigation bar on the left, and a dynamic content area that renders `pageContent`.
 *
 * @param {LayoutWrapperProps} props - The props passed to the component.
 * @returns {React.ReactElement} The rendered component.
 */
const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ pageContent }: LayoutWrapperProps): React.ReactElement => {
  return (
    <div className="flex h-screen flex-col min-h-screen select-none">
      {/* Full-width profile bar at the top of the page */}
      <div className="w-full">
        <ProfileBar/>
      </div>
      <div className="flex flex-row flex-1 overflow-hidden">
        {/* Sidebar navigation bar */}
        <NavigationBar/>
        {/* Main content area that takes remaining space */}
        <div className="flex-1 overflow-clip p-4 items-start justify-start">
          {/*{pageContent}*/}
            <Routes>
                <Route path="home" element={<HomePage/>} />
                <Route path="guidelines" element={<GuidelinePage/>} />
            </Routes>
        </div>
      </div>
    </div>
  );
};

export default LayoutWrapper;