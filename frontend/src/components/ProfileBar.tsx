import React from "react";
import Logo from "../assets/images/logo.svg"

interface ProfileBarProps {
    name: string;
    role: string;
    imageUrl: string;
}

const ProfileBar: React.FC<ProfileBarProps> = ({ name, role, imageUrl }) => {
    return (
        <div className="bg-white flex items-center py-5 px-10 shadow-profilebar-shadow border-b-2.7 border-border-gray font-semibold mr-8">
            <div className="flex items-center space-x-4">
                <img src={Logo} alt="Clockwise"  />
                <div className="w-32"/>
                <input type="text" placeholder="Search" className="input border border-gray-300 py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" />
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">This month</button>
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">By Project</button>
            </div>
            <div className="ml-auto flex items-center space-x-4">
                <img src={imageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
                <div className="flex flex-col items-start">
                    <span className="text-md font-semibold">{name}</span>
                    <span className="text-sm text-gray-500">{role}</span>
                </div>
            </div>
        </div>
    );
};

export default ProfileBar;
