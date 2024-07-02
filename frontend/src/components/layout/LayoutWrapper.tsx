import React from 'react';
import {Routes, Route } from 'react-router-dom';
import {useAuth} from "../../context/AuthContext";
import {routesConfig} from "../auth/RouteConfig";
import {PopupProvider, usePopup} from "../popup/PopupContext";
import ProfileBar from "../profile/ProfileBar";
import NavigationBar from "../navbar/NavigationBar";
import LayoutContentWithPopup from "./LayoutContentWithPopup";

/**
 * The LayoutWrapper component is responsible for providing the overall page layout.
 * It includes a profile bar at the top, a navigation bar on the left, and a dynamic content area that renders `pageContent`.
 *
 * @param {LayoutWrapperProps} props - The props passed to the component.
 * @returns {React.ReactElement} The rendered component.
 */
const LayoutWrapper = (): React.ReactElement => {
    const {role} = useAuth();
    const currentRoutes = role ? (routesConfig[role] || {}) : {};

    return (
      <PopupProvider>
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
                <LayoutContentWithPopup currentRoutes={currentRoutes}/>
                <Routes>
                    {/*{Object.entries(currentRoutes).map(([path, Component]) => (*/}
                    {/*    <Route key={path} path={path} element={<Component />} />*/}
                    {/*  ))}*/}

                </Routes>
            </div>
          </div>
        </div>
      </PopupProvider>
    );
};

export default LayoutWrapper;