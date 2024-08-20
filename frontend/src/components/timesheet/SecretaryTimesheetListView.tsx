import React from 'react';
import { Timesheet } from '../../interfaces/Timesheet';
import {User} from "../../interfaces/User";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import StatusLabel from "../status/Status";
import IconButton from "../navbar/IconButton";
import DownloadIcon from "images/download_icon.svg";
import {StatusType} from "../../interfaces/StatusType";
import UserInfoSecretaryView from "../UserInfoSecretaryView";

interface SecretaryTimesheetListViewProps {
  sheets: Timesheet[];
  hiwis: User[];
  supervisors: User[];
}

const SecretaryTimesheetListView: React.FC<SecretaryTimesheetListViewProps> = ({ sheets, hiwis, supervisors }) => {
  return (
    <div className="flex flex-col gap-2.5 overflow-y-auto max-h-[36rem]">
      {sheets.map((timesheet, index) => {
        const hiwi = hiwis.find(h => h.username === timesheet.username);
        return (
            <div key={index}
                 className="flex items-center px-4 py-3 pr-8 border-b bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap">
              <UserInfoSecretaryView
                  firstName={hiwi?.personalInfo.firstName ?? ""}
                  lastName={hiwi?.personalInfo.lastName ?? ""}
                  supervisor={hiwi?.supervisor ?? ""}
              />
              <div className="flex h-full">
                <StatusLabel status={timesheet.status}/>
              </div>
            </div>
        );
      })}
    </div>
  );
};

export default SecretaryTimesheetListView;
