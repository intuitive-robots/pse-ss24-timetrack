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
    <div className="flex flex-col gap-2.5">
      {sheets.map((timesheet, index) => {
        const hiwi = hiwis.find(h => h.username === timesheet.username); // Find corresponding hiwi for each timesheet
        return (
            <div key={index}
                 className="px-4 py-3 pr-8 border-b flex items-center bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg justify-between text-nowrap">
              {/*<div className="flex items-center gap-4">*/}
              {/*  <img src={ProfilePlaceholder} alt="Profile" className="w-10 h-10 rounded-full"/>*/}
              {/*  <div>*/}
              {/*      <p className="font-semibold">{hiwi?.personalInfo.firstName} {hiwi?.personalInfo.lastName}</p>*/}
              {/*      <p className="text-sm text-gray-500">Supervisor: {hiwi?.supervisor}</p>*/}
              {/*  </div>*/}
              {/*</div>*/}
              <UserInfoSecretaryView
                  firstName={hiwi?.personalInfo.firstName ?? ""}
                  lastName={hiwi?.personalInfo.lastName ?? ""}
                  supervisor={hiwi?.supervisor ?? ""}
                  profileImageUrl={ProfilePlaceholder}
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
