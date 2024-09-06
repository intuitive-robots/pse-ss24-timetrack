// Authors: Phil Gengenbach, Dominik Pollok, Alina Petri, José Ayala, Johann Kohl
import React from 'react';
import {useAuth} from "../../context/AuthContext";
import {routesConfig} from "../auth/RouteConfig";
import {PopupProvider} from "../popup/PopupContext";
import ProfileBar from "../profile/ProfileBar";
import NavigationBar from "../navbar/NavigationBar";
import LayoutContentWithPopup from "./LayoutContentWithPopup";
import {SearchProvider} from "../../context/SearchContext";

/**
 * The LayoutWrapper component is responsible for providing the overall page layout.
 * It includes a profile bar at the top, a navigation bar on the left, and a dynamic content area that renders `pageContent`.
 *
 * @returns {React.ReactElement} The rendered component.
 */
const LayoutWrapper = (): React.ReactElement => {
    const {role} = useAuth();
    const currentRoutes = role ? (routesConfig[role] || {}) : {};

    return (
      <PopupProvider>
          <SearchProvider>
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
                          <LayoutContentWithPopup currentRoutes={currentRoutes}/>
                      </div>
                  </div>
              </div>
          </SearchProvider>
      </PopupProvider>
    );
};

export default LayoutWrapper;