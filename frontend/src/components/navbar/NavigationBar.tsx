import React, { useState } from "react";
import ActionButton from "../input/ActionButton";
import AddUserIcon from "../../assets/images/add_user_icon.svg"
import {useAuth} from "../../context/AuthContext";
import {useNavigate} from "react-router-dom";
import navigationIcons from "./NavigationIcons";

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
  const [activeItem, setActiveItem] = useState<string>("Home");
  const { role } = useAuth();
  const navigate = useNavigate();

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
        return {

        };
    }
  }

  function handleItemClick(item: string) {
    setActiveItem(item);
    const path = `${item.toLowerCase().replace(/\s+/g, '-')}`;
    navigate(path);
  }

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
                  <img src={activeItem === item ? navigationIcons[item.replace(/\s+/, '')].active : navigationIcons[item.replace(/\s+/, '')].default}
                       className="mr-3 fill-amber-200" alt={`${item} icon`}/>
                  {item}
                </button>
            ))}
          </div>
        ))}
        <div className="mt-auto">
          <ActionButton
              icon={AddUserIcon}
              label="Add User"
              onClick={() => {
              }}
              bgColor="bg-purple-600"
              hover="hover:bg-purple-700"
          />
          <ActionButton
              icon={AddUserIcon}
              label="Set Deadline"
              onClick={() => {
              }}
              bgColor="bg-gray-700"
              hover="hover:bg-gray-800"
          />
        </div>
      </div>
    </div>
  );
};

export default NavigationBar;
