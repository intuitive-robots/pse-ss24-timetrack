import React, { useState, useEffect } from 'react';
import {getStatusType, StatusType} from "../../interfaces/StatusType";

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

// TODO: implement slide animation
/*
const StatusFilter: React.FC<StatusFilterProps> = ({ setFilter}) => {
    const statuses = ['View all', StatusType.Pending, StatusType.Waiting];

    const [activeStatus, setActiveStatus] = useState<string>(statuses[0]);
    const [translateClass, setTranslateClass] = useState<string>('translate-x-0'); // TODO neu


     useEffect(() => {
        const activeIndex = statuses.indexOf(activeStatus);
        const translateClasses = ['translate-x-0', 'translate-x-full', 'translate-x-[200%]'];
        setTranslateClass(translateClasses[activeIndex]);
    }, [activeStatus, statuses]);

    const handleStatusClick = (status : string) => {
        setActiveStatus(status);
        if (status === 'View all') {
            setFilter(null);
            return;
        } else {
            const statusType = getStatusType(status);
            setFilter(statusType !== undefined ? statusType : null);
        }
    };

    return (
        <div className="flex my-2">
            <div className="flex flex-row text-md font-medium px-3 py-2 bg-neutral-50 items-center rounded-lg">
                {statuses.map((status, index) => (
                    <div
                        key={status}
                        className={`relative flex items-center justify-center px-4 py-1.5 rounded-lg cursor-pointer ${
                            activeStatus === status ? 'bg-white shadow-lg transition-transform duration-300 transform translate-x-0' : 'bg-transparent'
                        } ${index !== statuses.length - 1 ? 'mr-2' : ''}`}
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
*/


const StatusFilter: React.FC<StatusFilterProps> = ({ setFilter}: StatusFilterProps): React.ReactElement => {
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
      <div className="flex flex-row text-md font-medium px-3 py-2 bg-[#FAFAFA] items-center rounded-xl transition-all">
        {statuses.map((status) => (
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

