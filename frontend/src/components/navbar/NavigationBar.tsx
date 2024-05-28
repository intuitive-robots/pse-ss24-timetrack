import React, { useState } from "react";

interface MenuItems {
  [key: string]: string[];
}

const NavigationBar: React.FC = () => {
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
          <button
            className="w-full py-2.5 px-4 bg-purple-600 text-white rounded-md shadow hover:bg-purple-700 transition-colors"
            onClick={() => {}}
          >
            Track Time
          </button>
          <button
            className="w-full py-2.5 px-4 bg-gray-700 text-white rounded-md shadow mt-4 hover:bg-gray-800 transition-colors"
            onClick={() => {}}
          >
            Add Vacation
          </button>
        </div>
      </div>
    </div>
  );
};

export default NavigationBar;
