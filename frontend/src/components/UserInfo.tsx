import React from 'react';
import {roleColors} from "../utils/RoleMapping";

interface UserInfoProps {
  name: string;
  lastName: string;
  username?: string;
  role: string;
  profileImageUrl: string;
}

/**
 * UserInfoSupervisorView component to display user profile information.
 *
 * @component
 * @param {UserInfoProps} props - The props passed to the UserInfoSupervisorView component.
 * @returns {React.ReactElement} A React Element that renders the user's profile information.
 */
const UserInfo: React.FC<UserInfoProps> = ({username, name, lastName, role, profileImageUrl}: UserInfoProps): React.ReactElement => {
  return (
    <div className="flex items-center space-x-3 mr-8 z-50">
      <img src={profileImageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
      <div className="flex flex-col items-start">
          <p className="text-card-title text-md font-semibold">
              {name} {lastName}
              {username && <span
                  className="text-gray-400 font-medium"> ({username})</span>}
          </p>
          <p className={`text-sm text-accent] font-medium ${roleColors[role]}`}>{role}</p>
      </div>
    </div>
  );
};

export default UserInfo;
