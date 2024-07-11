import React from 'react';
import DownloadIcon from "../assets/images/download_icon.svg";
import IconButton from "./navbar/IconButton";
import ListTileInfo from "./list/ListTileInfo";
import CalendarMonth from "./calendar/CalendarMonth";
import StatusLabel from "./status/Status";
import {StatusType} from "../interfaces/StatusType";
import UserInfoSecretaryView from "./UserInfoSecretaryView";
import {Roles} from "./auth/roles";

interface TimesheetTileProps {
  key: string;
  role: string;
  totalTime: number;
  vacationDays: number;
  overtime: number;
  status: StatusType;
  onDownload: () => void;
  projectName?: string;
  description?: string;
  month?: number;
  year?: number;
  name?: string;
  lastName?: string;
  supervisor?: string;
  profileImageUrl?: string;
}

const TimesheetTile: React.FC<TimesheetTileProps> = ({   role,
                                                         totalTime,
                                                         overtime,
                                                         status,
                                                         onDownload,
                                                         projectName,
                                                         description,
                                                         month,
                                                         year,
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

          {(role === Roles.Hiwi && month && year && projectName && description) && (
              <div className="flex gap-5">
                  <CalendarMonth month={month} year={year}/>
                  <div className="flex flex-col w-60 mt-1.5 gap-0.5">
                      <p className="text-md font-semibold">{projectName}</p>
                      <p className="text-sm font-semibold text-[#9F9F9F]">{description}</p>
                  </div>
              </div>
          )}
          {(role === Roles.Secretary && name && lastName && supervisor && profileImageUrl) && (
              <div className="flex gap-5">
                  <UserInfoSecretaryView
                      name={name}
                      lastName={lastName}
                      supervisor={supervisor}
                      profileImageUrl={profileImageUrl}
                  />
              </div>
          )}

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

export default TimesheetTile;
