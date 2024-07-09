import React from 'react';
import {roleColors} from "../utils/RoleMapping";

interface UserInfoSupervisorProps {
  name: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
}

/**
 * UserInfoSupervisorView component to display user profile information.
 *
 * @component
 * @param {UserInfoSupervisorProps} props - The props passed to the UserInfoSupervisorView component.
 * @returns {React.ReactElement} A React Element that renders the user's profile information.
 */
const UserInfoSupervisorView: React.FC<UserInfoSupervisorProps> = ({ name, lastName, role, profileImageUrl}: UserInfoSupervisorProps): React.ReactElement => {
  return (
    <div className="flex items-center space-x-3 mr-8 z-50">
      <img src={profileImageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
      <div className="flex flex-col items-start">
        <p className="text-card-title text-md font-semibold">{`${name} ${lastName}`}</p>
        <p className={`text-sm text-accent] font-medium ${roleColors[role]}`}>{role}</p>
      </div>
    </div>
  );
};

export default UserInfoSupervisorView;
