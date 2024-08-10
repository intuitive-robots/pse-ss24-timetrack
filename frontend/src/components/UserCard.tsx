import React from 'react';
import ListIconCardButton from "./input/ListIconCardButton";
import IconButton from "./navbar/IconButton";
import UserInfo from "./UserInfo";
import {EditUserIcon} from "../assets/iconComponents/EditUserIcon";
import {ViewUserIcon} from "../assets/iconComponents/ViewUserIcon";
import {RemoveIcon} from "../assets/iconComponents/RemoveIcon";
import {LockUserIcon} from "../assets/iconComponents/LockUserIcon";

interface UserCardProps {
  name: string;
  username?: string;
  lastName: string;
  role: string;
  profileImageUrl: string;
  isArchived?: boolean;
  onView: () => void;
  onEdit: () => void;
  onArchive: () => void;
  onUnlock: () => void;
  onDelete: () => void;
}

const UserCard: React.FC<UserCardProps> = ({ username, name, role, profileImageUrl, isArchived, lastName, onView, onEdit, onDelete, onArchive, onUnlock }) => {
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
              iconSrc={<ViewUserIcon/>}
              label="View"
              onClick={() => onView()}
          />
          <ListIconCardButton
              iconSrc={<EditUserIcon/>}
              label="Edit"
              onClick={() => onEdit()}
          />
              {isArchived ? (
          <ListIconCardButton
            iconSrc={<LockUserIcon />}
            label="Activate"
            onClick={() => onUnlock()}
          />
        ) : (
          <ListIconCardButton
            iconSrc={<LockUserIcon />}
            label="Archive"
            onClick={() => onArchive()}
          />
        )}
          <IconButton
              icon={<RemoveIcon className="text-[#B083FF]"/>}
              onClick={() => onDelete()}
              bgColor="bg-purple-100"
              hover="hover:bg-purple-200"
          />
          </div>

      </div>
  );
};

export default UserCard;
