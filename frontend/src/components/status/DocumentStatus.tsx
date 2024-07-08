import React from 'react';
import {StatusType} from "../../interfaces/StatusType";


interface StatusProps {
  status: StatusType;
}

const StatusLabel: React.FC<StatusProps> = ({ status }) => {
  const statusStyles = {
    [StatusType.Complete]: { bgColor: "bg-complete-bg", textColor: "text-complete-fg", iconColor: "fill-complete-fg" },
    [StatusType.Pending]: { bgColor: "bg-pending-bg", textColor: "text-pending-fg", iconColor: "fill-pending-fg"},
    [StatusType.Waiting]: { bgColor: "bg-waiting-bg", textColor: "text-waiting-fg", iconColor: "fill-waiting-fg"},
    [StatusType.Revision]: { bgColor: "bg-revision-bg", textColor: "text-revision-fg", iconColor: "fill-revision-fg"},
    [StatusType.NoTimesheet]: { bgColor: "bg-white", textColor: "text-black", iconColor: "fill-waiting-fg"},
  };

  const { bgColor, textColor, iconColor} = statusStyles[status];

  return (
      <div className={`flex flex-row gap-2 items-center justify-center w-36 py-2.5 px-5 rounded-lg ${bgColor} ${iconColor}`}>
        <svg width="15" height="18" viewBox="0 0 15 18" xmlns="http://www.w3.org/2000/svg">
            <path d="M8.91699 5.40023V0.767728C9.57224 1.01517 10.1674 1.39907 10.663 1.89398L13.1309 4.36323C13.6263 4.85827 14.0105 5.45328 14.2578 6.10856H9.62533C9.43746 6.10856 9.2573 6.03393 9.12446 5.90109C8.99162 5.76826 8.91699 5.58809 8.91699 5.40023ZM14.5837 7.86877V13.9002C14.5825 14.8392 14.209 15.7394 13.5451 16.4033C12.8811 17.0673 11.981 17.4408 11.042 17.4419H3.95866C3.0197 17.4408 2.11951 17.0673 1.45556 16.4033C0.791617 15.7394 0.418117 14.8392 0.416992 13.9002V3.98356C0.418117 3.0446 0.791617 2.14441 1.45556 1.48047C2.11951 0.816519 3.0197 0.443019 3.95866 0.441895L7.15678 0.441895C7.27224 0.441895 7.38628 0.451103 7.50033 0.458895V5.40023C7.50033 5.96381 7.72421 6.50431 8.12272 6.90283C8.52124 7.30134 9.06174 7.52523 9.62533 7.52523H14.5667C14.5745 7.63927 14.5837 7.75331 14.5837 7.86877ZM10.8465 10.5789C10.717 10.4429 10.5389 10.364 10.3512 10.3593C10.1635 10.3547 9.98168 10.4247 9.84562 10.5541L7.29562 12.9844C7.22748 13.0529 7.14604 13.1068 7.0563 13.1426C6.96657 13.1785 6.87044 13.1957 6.77383 13.193C6.67722 13.1904 6.58218 13.168 6.49455 13.1272C6.40692 13.0865 6.32856 13.0282 6.26428 12.956L5.13874 11.9544C5.06926 11.8925 4.98825 11.8448 4.90035 11.8142C4.81244 11.7835 4.71936 11.7705 4.62642 11.7758C4.43872 11.7866 4.26298 11.8715 4.13787 12.0118C4.07592 12.0813 4.02826 12.1623 3.99761 12.2502C3.96697 12.3381 3.95394 12.4312 3.95927 12.5241C3.97003 12.7118 4.05491 12.8876 4.19524 13.0127L5.28891 13.9859C5.68534 14.3825 6.22243 14.6062 6.78314 14.6085C7.34384 14.6107 7.88271 14.3913 8.28233 13.998L10.8217 11.5797C10.9576 11.4502 11.0366 11.2721 11.0412 11.0844C11.0459 10.8968 10.9758 10.7149 10.8465 10.5789Z"/>
        </svg>
        <p className={`text-md text-center font-semibold ${textColor}`}>{status}</p>
      </div>
  );
};

export default StatusLabel;
