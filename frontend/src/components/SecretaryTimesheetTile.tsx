import React from 'react';
import DownloadIcon from "../assets/images/download_icon.svg";
import IconButton from "./navbar/IconButton";
import ListTileInfo from "./list/ListTileInfo";
import CalendarMonth from "./calendar/CalendarMonth";
import StatusLabel from "./status/Status";
import {StatusType} from "../interfaces/StatusType";
import UserInfoSecretaryView from "./UserInfoSecretaryView";
import {Roles} from "./auth/roles";

interface SecretaryTimesheetTileProps {
  key: string;
  totalTime: number;
  vacationDays: number;
  overtime: number;
  status: StatusType;
  onDownload: () => void;
  name: string;
  lastName: string;
  supervisor: string;
  profileImageUrl: string;
}

const SecretaryTimesheetTile: React.FC<SecretaryTimesheetTileProps> = ({ totalTime,
                                                         overtime,
                                                         status,
                                                         onDownload,
                                                         name,
                                                         lastName,
                                                         supervisor,
                                                         profileImageUrl,
                                                         vacationDays
}) => {
    const totalTimeString = totalTime.toString() + "h";
    const vacationDaysString = vacationDays.toString() + " days";
    const overtimeString = overtime.toString() + "h";

    return (
      <div className="flex items-center px-4 py-2 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-center">

          <div className="flex gap-5">
              <UserInfoSecretaryView
                  name={name}
                  lastName={lastName}
                  supervisor={supervisor}
                  profileImageUrl={profileImageUrl}
              />
          </div>


          <ListTileInfo items={
              [totalTimeString, vacationDaysString, overtimeString]
          }/>

          <div className="flex flex-row gap-5 ml-auto">
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
