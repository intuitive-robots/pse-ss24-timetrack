import React, {useEffect, useState} from "react";
import {useAuth} from "../../context/AuthContext";
import {useLocation, useNavigate} from "react-router-dom";
import navigationIcons from "./NavigationIcons";
import {isValidRole} from "../auth/roles";
import {buttonConfigurations} from "./ActionButtonsConfig";
import PopupActionButton from "../input/PopupActionButton";
import { FaBars, FaTimes } from "react-icons/fa";
import RightArrow from "../../assets/images/arrow_right.svg";


interface MenuItems {
  [key: string]: string[];
}

/**
 * NavigationBar component that renders a vertical navigation bar with multiple sections and items.
 *
 * @component
 * @returns {React.ReactElement} A React Element that renders the navigation bar.
 */
const NavigationBar: React.FC = (): React.ReactElement => {
  const { role } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const getCurrentActiveItem = (): string => {
    // Extracts the last segment from the pathname, e.g., 'analysis' from '/app/analysis'
    const pathSegments = location.pathname.split('/');
    const activePath = pathSegments[pathSegments.length - 1];
    const items = Object.values(getMenuItemsByRole(role)).flat();
    const active = items.find(item => item.toLowerCase() === activePath.toLowerCase());
    return active || "Home";
  };

  const [activeItem, setActiveItem] = useState<string>(getCurrentActiveItem());
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState<boolean>(false);

  const menuItems = getMenuItemsByRole(role);

  function getMenuItemsByRole(role: string | null): MenuItems {
    switch (role) {
      case 'Admin':
        return {
          General: ["Home"],
          Data: ["Analysis"],
          Support: ["Guidelines"],
        };
      case 'Hiwi':
        return {
          General: ["Home"],
          Data: ["Analysis", "Documents"],
          Support: ["Contract", "Guidelines"],
        };
      case 'Supervisor':
        return {
          General: ["Home"],
          Data: ["Analysis"],
          Support: ["Employees", "Projects", "Guidelines"],
        };
      case 'Secretary':
        return {
          General: ["Home"],
          Data: ["Analysis", "Documents"],
          Support: ["Employees", "Guidelines"],
        };
      default:
        return {};
    }
  }

  const buttons = (role && isValidRole(role)) ? buttonConfigurations[role] || [] : [];

  function handleItemClick(item: string) {
    setActiveItem(item);
    const path = `${item.toLowerCase().replace(/\s+/g, '-')}`;
    navigate(path);
  }

  return (
    <div className="flex flex-col w-full lg:w-72 h-full shadow-navbar-shadow border-r-2.7 border-border-gray transition-all duration-200 ease-in-out">
      {/* Mobile Navbar Toggle */}
      <div className="lg:hidden flex items-center justify-between p-4">
        {/*<div className="text-xl font-semibold">Logo</div>*/}
        <button
            className="p-1.5 mr-8 rounded-md bg-neutral-100 border-[1.4px] border-[#eee] hover:bg-neutral-200 z-50"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
          <div className={`w-6 h-6 transform transition-transform duration-200 ${isMobileMenuOpen ? 'rotate-90' : 'rotate-0'}`}>
            <img src={RightArrow} alt="RightArrow" className="w-6 h-6"/>
          </div>
        </button>
      </div>

      {/* Navigation Items */}
      <div
          className={`h-full py-14 px-6 gap-6 flex flex-col font-semibold ${isMobileMenuOpen ? 'block' : 'hidden'} lg:block`}>
        {Object.keys(menuItems).map((section) => (
            <div key={section}>
              <div className="flex text-md tracking-wide text-[#BFBFBF] mb-2">
              {section}
              </div>
            {menuItems[section].map((item) => (
              <button
                key={item}
                className={`flex items-center text-left w-full py-2 px-4 rounded-md
                  ${
                    activeItem === item
                      ? "bg-navbar-selected-bg text-gray-800 py-2 transition duration-300 ease-in-out transform"
                      : "text-gray-600 hover:bg-navbar-selected-bg"
                  }`}
                onClick={() => handleItemClick(item)}
              >
                <img
                  src={activeItem === item ? navigationIcons[item.replace(/\s+/, '')].active : navigationIcons[item.replace(/\s+/, '')].default}
                  className="mr-3 fill-amber-200" alt={`${item} icon`} />
                {item}
              </button>
            ))}
          </div>
        ))}
        <div className="mt-auto">
          {buttons.length > 0 && (
            <PopupActionButton
              icon={buttons[0].icon}
              label={buttons[0].label}
              popupComponent={buttons[0].popup}
              primary={true}
            />
          )}
          {buttons.length > 1 && (
            <PopupActionButton
              icon={buttons[1].icon}
              label={buttons[1].label}
              popupComponent={buttons[1].popup}
              secondary={true}
            />
          )}
        </div>
      </div>
    </div>
  );
};
  /*
  return (
    <div className="flex-col w-72 h-full shadow-navbar-shadow border-r-2.7 border-border-gray transition-all duration-200 ease-in-out">
      <div className="h-full py-14 px-6 gap-6 flex flex-col font-semibold">
        {Object.keys(menuItems).map((section) => (
            <div key={section}>
              <div className="flex text-md tracking-wide text-[#BFBFBF] mb-2">
                {section}
              </div>
              {menuItems[section].map((item) => (
                  <button
                      key={item}
                      className={`flex items-center text-left w-full py-2 px-4 rounded-md
                                            ${
                          activeItem === item
                              ? "bg-navbar-selected-bg text-gray-800 py-2 transition duration-300 ease-in-out transform"
                              : "text-gray-600 hover:bg-navbar-selected-bg"
                      }`}
                      onClick={() => handleItemClick(item)}
                  >
                    <img
                        src={activeItem === item ? navigationIcons[item.replace(/\s+/, '')].active : navigationIcons[item.replace(/\s+/, '')].default}
                        className="mr-3 fill-amber-200" alt={`${item} icon`}/>
                    {item}
                  </button>
              ))}
            </div>
        ))}
        <div className="mt-auto">
          {buttons.length > 0 && (
              <PopupActionButton
                  icon={buttons[0].icon}
                  label={buttons[0].label}
                  popupComponent={buttons[0].popup}
                  primary={true}
              />
          )}
          {buttons.length > 1 && (
              <PopupActionButton
                  icon={buttons[1].icon}
                  label={buttons[1].label}
                  popupComponent={buttons[1].popup}
                  secondary={true}
              />
          )}
        </div>
      </div>
    </div>
  );
};

   */

export default NavigationBar;
