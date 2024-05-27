import React from "react";
import Logo from "../assets/images/logo.svg"

interface ProfileBarProps {
    name: string;
    role: string;
    imageUrl: string;
}

const ProfileBar: React.FC<ProfileBarProps> = ({ name, role, imageUrl }) => {
    return (
        <div className="bg-white flex items-center py-6 px-10 shadow-profilebar-shadow border-b-2.7 border-border-gray">
            <div className="flex items-center space-x-4">
                <img src={Logo} alt="Clockwise"  />
                <div className="w-32"/>
                <input type="text" placeholder="Search" className="input border border-gray-300 py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" />
                <button className="btn bg-gray-200 hover:bg-gray-300 text-md text-black py-2 px-4 rounded-lg">This month</button>
                <button className="btn bg-gray-200 hover:bg-gray-300 text-black py-2 px-4 rounded-lg">By Project</button>
            </div>
            <div className="ml-auto flex items-center space-x-2">
                <img src={imageUrl} alt="User Avatar" className="h-10 w-10 rounded-full"/>
                <div className="flex flex-col items-start">
                    <span className="text-sm font-semibold">{name}</span>
                    <span className="text-xs text-gray-500">{role}</span>
                </div>
            </div>
        </div>
    );
};

export default ProfileBar;
