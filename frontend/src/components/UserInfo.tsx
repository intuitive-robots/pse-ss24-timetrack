import React from 'react';
import {roleColors} from "../utils/RoleMapping";
import DynamicProfilePicture from "./profile/DynamicProfilePicture";

interface UserInfoProps {
  name: string;
  lastName: string;
  username?: string;
  role: string;
  isProfileBar?: boolean;
  loading?: boolean;
}

/**
 * UserInfoSupervisorView component to display user profile information.
 *
 * @component
 * @param {UserInfoProps} props - The props passed to the UserInfoSupervisorView component.
 * @returns {React.ReactElement} A React Element that renders the user's profile information.
 */
const UserInfo: React.FC<UserInfoProps> = ({username, name, lastName, role, loading = false, isProfileBar}: UserInfoProps): React.ReactElement => {
  return (
    <div className={`flex items-center space-x-3 z-50 transition-all duration-300 ease-in-out ${loading ? 'blur-sm' : 'blur-none'}`}>
      {/*<img src={profileImageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>*/}
        <DynamicProfilePicture firstName={name} lastName={lastName}/>
        <div className="flex flex-col items-start">
          <p className={`text-card-title text-md font-semibold ${loading ? 'blur-sm' : 'blur-none'}`}>
              {name} {lastName}
              {username && <span className="text-gray-400 font-medium"> ({username})</span>}
          </p>
          <p className={`text-sm text-accent font-medium ${roleColors[role]} ${loading ? 'blur-sm' : 'blur-none'}`}>{role}</p>
        </div>
    </div>
  );
};

export default UserInfo;
