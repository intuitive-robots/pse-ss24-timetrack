import React from 'react';
import {StatusType} from "../../interfaces/StatusType";


interface StatusProps {
  status: StatusType;
}

const StatusLabel: React.FC<StatusProps> = ({ status }) => {
  const statusStyles = {
    [StatusType.Complete]: { bgColor: "bg-complete-bg", textColor: "text-complete-fg" },
    [StatusType.Pending]: { bgColor: "bg-pending-bg", textColor: "text-pending-fg" },
    [StatusType.Waiting]: { bgColor: "bg-waiting-bg", textColor: "text-waiting-fg" },
    [StatusType.Revision]: { bgColor: "bg-revision-bg", textColor: "text-revision-fg" },
    [StatusType.NoTimesheet]: { bgColor: "bg-white", textColor: "text-black" },
    [StatusType.Error]: { bgColor: "bg-revision-bg", textColor: "text-revision-fg" },
  };

  const { bgColor, textColor } = statusStyles[status] || { bgColor: "bg-white", textColor: "text-black" };

  return (
    <div className={`flex items-center justify-center w-28 px-6 py-0.5 rounded-lg ${bgColor}`}>
      <p className={`text-md text-center font-semibold ${textColor}`}>{status}</p>
    </div>
  );
};

export default StatusLabel;
