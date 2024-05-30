import React from 'react';
import UserInfo from "./UserInfo";

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
          <button
              className="ml-auto p-2 mx-1 rounded border text-sm flex items-center"
              onClick={onView}
          >
              <i className="fas fa-eye mr-2"></i>
              View
          </button>
          <button
              className="p-2 mx-1 rounded border text-sm flex items-center"
              onClick={onEdit}
          >
              <i className="fas fa-edit mr-2"></i>
              Edit
          </button>
          <button
              className="p-2 mx-1 rounded border text-sm flex items-center text-red-500"
              onClick={onDelete}
          >
              <i className="fas fa-times mr-2"></i>
          </button>
      </div>
  );
};

export default UserCard;
