import React from "react";
import Logo from "../assets/images/logo.svg"
import RightArrow from "../assets/images/arrow_right.svg"
import { logout } from "../services/AuthService";
import {useNavigate} from "react-router-dom";

interface ProfileBarProps {
    name: string;
    role: string;
    imageUrl: string;
}

/**
 * The ProfileBar component renders a user interface at the top of a page, including a logo, search input,
 * navigation buttons, and user profile information. It provides a consistent top bar across different
 * parts of the application.
 *
 * The component is structured to display the following:
 * - A logo on the left side.
 * - A search bar for user input.
 * - Navigation buttons for temporal filters such as 'This month' and 'By Project'.
 * - User's profile image with their name and role on the right side of the bar.
 * - An arrow button next to the user's information for additional options or navigation.
 *
 * @component
 * @param {ProfileBarProps} props - The props passed to the ProfileBar component.
 * @returns {React.ReactElement} A React Element representing the user profile bar.
 */
const ProfileBar: React.FC<ProfileBarProps> = ({ name, role, imageUrl }: ProfileBarProps): React.ReactElement => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/login');
        } catch (error) {
            console.error('Logout failed', error);
        }
    };

    return (
        <div className="bg-white flex items-center py-5 px-10 shadow-profilebar-shadow border-b-2.7 border-border-gray font-semibold">
            <div className="flex items-center space-x-4">
                <img src={Logo} alt="Clockwise"  />
                <div className="w-32"/>
                <input type="text" placeholder="Search" className="input border border-gray-300 py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" />
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">This month</button>
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">By Project</button>
            </div>
            <div className="ml-auto flex items-center space-x-4 mr-4">
                <img src={imageUrl} alt="User Avatar" className="h-12 w-12 rounded-full"/>
                <div className="flex flex-col items-start">
                    <span className="text-md font-semibold">{name}</span>
                    <span className="text-sm text-gray-500">{role}</span>
                </div>
                <button
                    className="p-1.5 rounded-md bg-neutral-100 border-[1.4px] border-[#eee] hover:bg-neutral-200"
                    onClick={handleLogout}
                >
                    <img src={RightArrow} alt="RightArrow"/>
                </button>
            </div>
        </div>
    );
};

export default ProfileBar;