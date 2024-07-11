import React from 'react';
import UserInfoSupervisorView from "./UserInfo";
import ListIconCardButton from "./input/ListIconCardButton";
import CheckTimesheetIcon from "../assets/images/check_timesheet_icon.svg"
import StatusLabel from "./status/Status";
import {StatusType} from "../interfaces/StatusType";
import {User} from "../interfaces/Hiwi";


interface HiwiCardProps {
  name: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
  status: StatusType;
  onCheck: () => void;
}

const HiwiTimesheetCard: React.FC<HiwiCardProps> = ({ name, role, profileImageUrl, lastName, status, onCheck}) => {
  return (
      <div className="flex items-center p-4 bg-white shadow rounded-lg mb-4">
          <UserInfoSupervisorView
              name={name}
              lastName={lastName}
              role={role}
              profileImageUrl={profileImageUrl}
          />
          <div className="flex ml-auto gap-8">
              <ListIconCardButton
                  iconSrc={CheckTimesheetIcon}
                  label="Check"
                  onClick={onCheck}
              />
              <div className="pr-6 items-center justify-center">
                  <StatusLabel status={status} />
              </div>

          </div>

      </div>
  );
};

export default HiwiTimesheetCard;
