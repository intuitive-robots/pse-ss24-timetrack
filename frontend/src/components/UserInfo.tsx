import React from 'react';

interface UserInfoProps {
  name: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
}

/**
 * UserInfo component to display user profile information.
 *
 * @component
 * @param {UserInfoProps} props - The props passed to the UserInfo component.
 * @returns {React.ReactElement} A React Element that renders the user's profile information.
 */
const UserInfo: React.FC<UserInfoProps> = ({ name, lastName, role, profileImageUrl }: UserInfoProps): React.ReactElement => {
  return (
    <div className="flex items-center space-x-4 mr-8">
      <img src={profileImageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
      <div className="flex flex-col items-start mt-0.5">
        <span className="text-md font-semibold">{`${name} ${lastName}`}</span>
        <span className="text-sm text-[#BCBCBC] font-medium">{role}</span>
      </div>
    </div>
  );
};

export default UserInfo;
