import React, { useState } from "react";
import ActionButton from "../input/ActionButton";
import AddUserIcon from "../../assets/images/add_user_icon.svg"

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

  const menuItems: MenuItems = {
    General: ["Home"],
    Data: ["Analysis", "Documents"],
    Support: ["Contract", "Guidelines"],
  };

  return (
    <div className="flex-col w-72 h-full shadow-navbar-shadow border-r-2.7 border-border-gray">
      <div className="h-full py-14 px-6 gap-6 flex flex-col font-semibold">
        {Object.keys(menuItems).map((section) => (
          <div key={section}>
            <div className="flex text-md tracking-wide text-[#BFBFBF] mb-2">
              {section}
            </div>
            {menuItems[section].map((item) => (
              <button
                key={item}
                className={`text-left w-full py-1.5 px-4 rounded-md
                                            ${
                                              activeItem === item
                                                ? "bg-navbar-selected-bg text-gray-800"
                                                : "text-gray-600 hover:bg-navbar-selected-bg"
                                            }`}
                onClick={() => setActiveItem(item)}
              >
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
              hoverBgColor="bg-purple-700"
          />
          <ActionButton
              icon={AddUserIcon}
              label="Set Deadline"
              onClick={() => {
              }}
              bgColor="bg-gray-700"
              hoverBgColor="bg-gray-800"
          />
        </div>
      </div>
    </div>
  );
};

export default NavigationBar;
