import React, { useState } from 'react';
import { motion} from 'framer-motion';
import {Roles} from "../auth/roles";


const RoleFilter: React.FC<{ onRoleChange: (role: string) => void }> = ({ onRoleChange }) => {
  const [activeRole, setActiveRole] = useState<string>("View all");
  const filterRoles = ["View all", ...Object.values(Roles), "Archived"];

  const handleRoleClick = (role: string) => {
    setActiveRole(role);
    onRoleChange(role);
  };

  return (
    <div className="flex my-2">
      <div className="flex flex-row text-md font-medium px-3 py-2 bg-neutral-50 items-center rounded-lg">
        {filterRoles.map((role) => (
          <div
            key={role}
            className={`relative flex items-center justify-center px-6 py-1.5 rounded-lg transition-all duration-300 cursor-pointer ${
              activeRole === role ? 'bg-white shadow-card-shadow' : 'bg-transparent'
            }`}
            onClick={() => handleRoleClick(role)}
          >
            {activeRole === role && (
              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1.05 }}
                exit={{ scale: 0.95 }}
                className="absolute inset-0 rounded-lg bg-white -z-10"
              />
            )}
            <p className={`${activeRole === role ? 'text-filter-active' : 'text-[#606060]'}`}>
              {role}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RoleFilter;
