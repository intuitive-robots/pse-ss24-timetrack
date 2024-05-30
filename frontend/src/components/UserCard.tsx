import React from 'react';

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
          <div className="flex items-center space-x-4 mr-8">
              <img src={profileImageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
              <div className="flex flex-col items-start">
                    <span
                        className="text-md font-semibold">{name + " " + lastName}</span>
                  <span className="text-sm text-gray-500">{role}</span>
              </div>
          </div>
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
