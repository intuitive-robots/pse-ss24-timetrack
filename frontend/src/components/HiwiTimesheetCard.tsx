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
      <div className="flex items-center p-4 pr-6 bg-white shadow-card-shadow border-1.7 border-card-gray rounded-lg mb-4">
          <UserInfoSupervisorView
              name={name}
              lastName={lastName}
              role={role}
          />
          <div className="flex ml-auto gap-8">
              <ListIconCardButton
                  iconSrc={CheckTimesheetIcon}
                  label="Check"
                  onClick={onCheck}
              />
              <StatusLabel status={status} />
          </div>

      </div>
  );
};

export default HiwiTimesheetCard;
