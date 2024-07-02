import React, {useState} from "react";
import Logo from "../../assets/images/logo.svg";
import RightArrow from "../../assets/images/arrow_right.svg";
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../context/AuthContext';
import UserInfo from "../UserInfo";
import ProfilePicture from "../../assets/images/profile_placeholder.svg"
import SearchInput from "./SearchInput";

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
 * @returns {React.ReactElement} A React Element representing the user profile bar.
 */
const ProfileBar: React.FC = (): React.ReactElement => {
  const navigate = useNavigate();
  const { role, user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);

  return (
    <div className="bg-white flex items-center py-5 px-10 gap-5 shadow-profilebar-shadow border-b-2.7 border-border-gray font-semibold text-nowrap transition-all duration-300 ease-in-out ">
        <div className="flex items-center space-x-4">
          <img src={Logo} alt="Clockwise" />
          <div className="transition-all duration-400 ease-in-out md:w-12 lg:w-32" />
            <SearchInput placeholder="Search" />

          <div className="flex gap-3">
              <button
                  className="btn border hover:bg-gray-200 text-sm text-light-navGray h-full py-2 px-6 rounded-lg hidden md:flex">This
                  month
              </button>
              <button className="btn border hover:bg-gray-200 text-sm text-light-navGray h-full py-2 px-6 rounded-lg hidden lg:flex">By
                  Project
              </button>
          </div>
        </div>
        <div className="ml-auto relative">
            {user && (
                <div className="flex items-center cursor-pointer">
                    <UserInfo
                        name={user.personalInfo.firstName}
                        lastName={user.personalInfo.lastName}
                        role={role || "N/A"}
                        profileImageUrl={user.profileImageUrl || ProfilePicture}
                    />
                </div>
            )}

            {isDropdownOpen && (
                <div className="absolute left-0 mt-2 w-52 bg-white rounded-md shadow-lg py-1 z-500">
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">My
                        Profile
                    </button>
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Change
                        Password
                    </button>
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Help
                    </button>
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                            onClick={handleLogout}>Sign Out
                    </button>
                </div>
            )}
        </div>

        <button
            className="p-1.5 mr-8 rounded-md bg-neutral-100 border-[1.4px] border-[#eee] hover:bg-neutral-200"
            onClick={toggleDropdown}
        >
            <img src={RightArrow} alt="RightArrow"/>
        </button>

    </div>
  );
};

export default ProfileBar;
