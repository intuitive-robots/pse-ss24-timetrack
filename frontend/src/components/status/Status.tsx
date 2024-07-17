import React from 'react';
import {StatusType} from "../../interfaces/StatusType";


interface StatusProps {
  status: StatusType;
}

const StatusLabel: React.FC<StatusProps> = ({ status }) => {
  const statusStyles = {
    [StatusType.Complete]: { bgColor: "bg-complete-bg", textColor: "text-complete-fg", fontWeight: "font-semibold" },
    [StatusType.Pending]: { bgColor: "bg-pending-bg", textColor: "text-pending-fg", fontWeight: "font-semibold" },
    [StatusType.Waiting]: { bgColor: "bg-waiting-bg", textColor: "text-waiting-fg", fontWeight: "font-semibold" },
    [StatusType.Revision]: { bgColor: "bg-revision-bg", textColor: "text-revision-fg", fontWeight: "font-semibold" },
    [StatusType.NoTimesheet]: { bgColor: "bg-gray-50", textColor: "text-gray-500", fontWeight: "font-semibold" },
    [StatusType.Error]: { bgColor: "bg-error-bg", textColor: "text-error-fg", fontWeight: "font-light" },
  };

  const { bgColor, textColor, fontWeight } = statusStyles[status] || { bgColor: "bg-white", textColor: "text-black" };

  return (
    <div className={`flex items-center justify-center w-28 px-6 py-0.5 rounded-lg ${bgColor}`}>
      <p className={`text-md text-center ${fontWeight} ${textColor}`}>{status}</p>
    </div>
  );
};

export default StatusLabel;
