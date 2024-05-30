import React from 'react';
import UserInfo from "./UserInfo";
import ListIconCardButton from "./navbar/ListIconCardButton";

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
      <div className="flex items-center p-4 bg-white shadow rounded-lg mb-4">
          <UserInfo
              name={name}
              lastName={lastName}
              role={role}
              profileImageUrl={profileImageUrl}
          />
          <div className="flex ml-auto gap-4">
              <ListIconCardButton
              iconSrc=""
              label="View"
              onClick={() => {}}
          />
          <ListIconCardButton
              iconSrc=""
              label="Edit"
              onClick={() => {}}
          />
          <ListIconCardButton
              iconSrc=""
              label="Delete"
              onClick={() => {}}
          />
          </div>

      </div>
  );
};

export default UserCard;
