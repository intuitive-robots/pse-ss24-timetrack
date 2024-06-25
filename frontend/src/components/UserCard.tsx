import React from 'react';
import UserInfo from "./UserInfo";
import ListIconCardButton from "./navbar/ListIconCardButton";
import EditUserIcon from "../assets/images/edit_user_icon.svg"
import ViewUserIcon from "../assets/images/view_icon.svg"
import RemoveIcon from "../assets/images/remove_icon.svg"
import IconButton from "./navbar/IconButton";

interface UserCardProps {
  name: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
  onView: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

const UserCard: React.FC<UserCardProps> = ({ name, role, profileImageUrl, lastName, onView, onEdit, onDelete }) => {
  return (
      <div className="flex items-center p-4 shadow-card-shadow border-1.7 border-card-gray rounded-lg mb-4">
          <UserInfo
              name={name}
              lastName={lastName}
              role={role}
              profileImageUrl={profileImageUrl}
          />
          <div className="flex ml-auto gap-5">
              <ListIconCardButton
              iconSrc={ViewUserIcon}
              label="View"
              onClick={() => {}}
          />
          <ListIconCardButton
              iconSrc={EditUserIcon}
              label="Edit"
              onClick={() => {}}
          />
          <IconButton
              icon={RemoveIcon}
              onClick={() => {}}
              bgColor="bg-purple-100"
              hover="hover:bg-purple-200"
          />
          </div>

      </div>
  );
};

export default UserCard;
