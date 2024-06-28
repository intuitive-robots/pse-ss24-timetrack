import React, { useState } from 'react';
import {getStatusType, StatusType} from "../interfaces/StatusType";

interface StatusFilterProps {
    setFilter: (status: StatusType | null) => void;
}

/**
 * Status Filter component that renders the status filter bar with the correct activated status.
 *
 * @component
 * @param {StatusFilterProps} props - The props passed to the Status component.
 * @returns {React.ReactElement} A React Element that renders the status filter bar with the correct activated status.
 */

const StatusFilter: React.FC<StatusFilterProps> = ({ setFilter}) => {
  const statuses = ['View all', StatusType.Pending, StatusType.Waiting];

  const [activeStatus, setActiveStatus] = useState<string>(statuses[0]);

  const handleStatusClick = (status : string) => {
    setActiveStatus(status);
    if (status === 'View all') {
        setFilter(null);
        return;
    }

    const statusType = getStatusType(status);
    setFilter(statusType !== undefined ? statusType : null);
  };

  return (
      <div className="flex my-2">
        <div className="flex flex-row text-md font-medium px-3 py-2 bg-neutral-50 items-center rounded-lg">
          {statuses.map((status) => (
              <div
                  key={status}
                  className={`relative flex items-center justify-center px-6 py-1.5 rounded-lg transition-all duration-300 cursor-pointer ${
                      activeStatus === status ? 'bg-white shadow-lg' : 'bg-transparent'
                  }`}
                  onClick={() => handleStatusClick(status)}
              >
                {activeStatus === status && (
                    <div className="absolute inset-0 rounded-lg bg-white -z-10 transform scale-105"></div>
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
