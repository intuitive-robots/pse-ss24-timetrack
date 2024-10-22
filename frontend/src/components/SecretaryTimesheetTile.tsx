import React from 'react';
import DownloadIcon from "../assets/images/download_icon.svg";
import IconButton from "./navbar/IconButton";
import ListTileInfo from "./list/ListTileInfo";
import StatusLabel from "./status/Status";
import {StatusType} from "../interfaces/StatusType";
import UserInfoSecretaryView from "./UserInfoSecretaryView";
import {minutesToHourMinuteFormatted} from "../utils/TimeUtils";

interface SecretaryTimesheetTileProps {
  totalTime: string;
  vacationMinutes: number;
  overtime: string;
  status: StatusType;
  onDownload: () => void;
  username: string;
  firstName: string;
  lastName: string;
  supervisorName: string;
}

const SecretaryTimesheetTile: React.FC<SecretaryTimesheetTileProps> = ({ totalTime,
                                                         overtime,
                                                         status,
                                                         onDownload, username,
                                                         firstName,
                                                         lastName,
                                                           supervisorName,
                                                         vacationMinutes
}) => {
    const vacationDaysString = vacationMinutes ? minutesToHourMinuteFormatted(vacationMinutes) : "0h"

    return (
      <div className="flex items-center px-4 gap-6 py-3 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap">
          <div className="flex gap-5 w-60">
              <UserInfoSecretaryView
                  firstName={firstName}
                  lastName={lastName}
                  supervisor={supervisorName}
              />
          </div>


          <ListTileInfo items={
              [totalTime, vacationDaysString, overtime]}
              gap={"lg:gap-12 gap-8 transition-all"}
          />

          <div className="flex flex-row gap-5 items-center">
              <StatusLabel status={status}/>
              <IconButton
                  icon={DownloadIcon}
                  onClick={() => onDownload()}
                  bgColor= {`border-1.7 border-[#E0E0E0] ${status === StatusType.Complete ? "bg-white" : "bg-gray-100 opacity-70 cursor-auto"}`}
                  size={"px-5 py-2.5"}
                  hover={status === StatusType.Complete ? 'hover:bg-gray-200' : ''}
              />
          </div>

      </div>
  );
};

export default SecretaryTimesheetTile;
