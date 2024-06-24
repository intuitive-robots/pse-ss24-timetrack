import React from 'react';
import UserInfo from "./UserInfo";
import ListIconCardButton from "./navbar/ListIconCardButton";
import CheckTimesheetIcon from "../assets/images/check_timesheet_icon.svg"
import Status from "./navbar/Status";


interface HiwiCardProps {
  name: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
  onCheck: () => void;
}

const HiwiCard: React.FC<HiwiCardProps> = ({ name, role, profileImageUrl, lastName, onCheck}) => {
  return (
      <div className="flex items-center p-4 bg-white shadow rounded-lg mb-4">
          <UserInfo
              name={name}
              lastName={lastName}
              role={role}
              profileImageUrl={profileImageUrl}
          />
          <div className="flex ml-auto gap-8">
              <ListIconCardButton
                  iconSrc={CheckTimesheetIcon}
                  label="Check"
                  onClick={() => {
                  }}
              />
              <div className="pr-6">
                  <Status label={'Warning'} bgColor={'[#FCC6C6]'} color={'[#F97D7D]'} /> {/*TODO: Farben an Status anpassen, aktuell noch hard gecodet*/}
              </div>

          </div>

      </div>
  );
};

export default HiwiCard;
