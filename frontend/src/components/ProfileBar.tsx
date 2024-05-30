import React from "react";
import Logo from "../assets/images/logo.svg"
import RightArrow from "../assets/images/arrow_right.svg"
import {useNavigate} from "react-router-dom";
import { useAuth } from '../context/AuthContext'
import UserInfo from "./UserInfo";

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
const ProfileBar: React.FC<ProfileBarProps> = ({imageUrl }: ProfileBarProps): React.ReactElement => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/login');
        } catch (error) {
            console.error('Logout failed', error);
        }
    };

    return (
        <div
            className="bg-white flex items-center py-5 px-10 shadow-profilebar-shadow border-b-2.7 border-border-gray font-semibold">
            <div className="flex items-center space-x-4 mr-auto">
                <img src={Logo} alt="Clockwise"/>
                <div className="w-32"/>
                <input type="text" placeholder="Search"
                       className="input border border-gray-300 py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"/>
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">This
                    month
                </button>
                <button className="btn border hover:bg-gray-200 text-sm text-light-navGray py-2 px-6 rounded-lg">By
                    Project
                </button>
            </div>

            <UserInfo
                name={user?.personalInfo.firstName}
                lastName={user?.personalInfo.lastName}
                role={user?.role}
                profileImageUrl={imageUrl}
            />
            <button
                className="p-1.5 mr-8 rounded-md bg-neutral-100 border-[1.4px] border-[#eee] hover:bg-neutral-200"
                onClick={handleLogout}
            >
                <img src={RightArrow} alt="RightArrow"/>
            </button>
        </div>
    );
};

export default ProfileBar;