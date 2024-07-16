import React, { useState, useEffect } from 'react';
import {getStatusType, StatusType} from "../../interfaces/StatusType";

interface StatusFilterProps {
    setFilter: (status: StatusType | null) => void;
    filterStatuses?: StatusType[];
}

/**
 * Status Filter component that renders the status filter bar with the correct activated status.
 *
 * @component
 * @param {StatusFilterProps} props - The props passed to the Status component.
 * @returns {React.ReactElement} A React Element that renders the status filter bar with the correct activated status.
 */


const StatusFilter: React.FC<StatusFilterProps> = ({ setFilter, filterStatuses = []}: StatusFilterProps): React.ReactElement => {
    const availableStatuses = ['View All', ...filterStatuses];
    const [activeStatus, setActiveStatus] = useState<string>(availableStatuses[0]);

  const handleStatusClick = (status : string) => {
    setActiveStatus(status);
    if (status === 'View all') {
        setFilter(null);
        return;
    }

    const statusType = getStatusType(status);
    setFilter(statusType !== undefined ? statusType : null);
    console.log("Status Filter: " + status);
    console.log("Status Filter: " + getStatusType(status));
  };

  return (
    <div className="flex my-2">
      <div className="flex flex-row text-md font-medium px-3 py-2 bg-[#FAFAFA] items-center rounded-xl transition-all">
        {availableStatuses.map((status) => (
          <div
            key={status}
            className={`relative flex items-center justify-center px-6 py-1.5 rounded-lg transition-all duration-300 cursor-pointer ${
              activeStatus === status ? 'bg-white shadow-filter-shadow' : 'bg-transparent'
            }`}
            onClick={() => handleStatusClick(status)}
          >
            {activeStatus === status && (
              <div className="absolute inset-0 rounded-lg bg-white -z-10 transform scale-105 animate-slideIn"></div>
            )}
            <p className={`${activeStatus === status ? 'text-filter-active' : 'text-[#606060]'}`}>
              {status}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StatusFilter;

