import React, {useState} from "react";
import RightArrow from "../../assets/images/arrow_right.svg";
import UserIcon from "../../assets/images/dropdown/user_icon.svg";
import ChangePasswordIcon from "../../assets/images/dropdown/change_password.svg";
import LogoutIcon from "../../assets/images/dropdown/logout.svg";
import HelpIcon from "../../assets/images/dropdown/help.svg";
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../context/AuthContext';
import UserInfoSupervisorView from "../UserInfo";
import ProfilePicture from "../../assets/images/profile_placeholder.svg"
import SearchInput from "./SearchInput";
import DropdownMenuButton from "../dropdown/DropdownMenuButton";
import HorizontalSeparator from "../../shared/HorizontalSeparator";
import {usePopup} from "../popup/PopupContext";
import PasswordResetPopup from "../popup/PasswordResetPopup";
import {ClockwiseIcon} from "../../assets/iconComponents/ClockwiseIcon";
import UserInfo from "../UserInfo";
import {NotificationShowcase} from "../notification/NotificationShowcase";

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
  const { role, user, logout, isLoading } = useAuth();

  const {openPopup} = usePopup();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);
      navigate('/login');
    }
    window.location.reload();
  };

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);

  return (
    <div className="bg-white flex items-center py-5 px-10 shadow-profilebar-shadow border-b-2.7 border-border-gray font-semibold text-nowrap transition-all duration-300 ease-in-out ">
        <div className="flex items-center space-x-4">
            <ClockwiseIcon/>
            <div className="transition-all duration-500 ease-in-out md:w-12 lg:w-32" />
            <div className="hidden sm:flex">
                <SearchInput placeholder="Search" />
            </div>

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


        <div className="flex gap-2 items-center relative ml-auto md:pl-8 pl-2 transition-all duration-500 ease-in-out">
            <div className="z-50 mr-6">
                <NotificationShowcase/>
            </div>
            <div className="flex items-center z-50 mr-4">
                <UserInfo
                    name={user ? user.personalInfo.firstName : "Max"}
                    lastName={user ? user.personalInfo.lastName : "Muster"}
                    role={user ? role || "N/A" : "Loading"}
                    profileImageUrl={user ? user.profileImageUrl || ProfilePicture : ProfilePicture}
                    loading={user === null || isLoading}
                />
            </div>

            <button
                className="p-1.5 mr-8 rounded-md bg-neutral-100 border-[1.4px] border-[#eee] hover:bg-neutral-200 z-50"
                onClick={toggleDropdown}
            >
                <div
                    className={`transform transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : 'rotate-0'}`}>
                    <img src={RightArrow} alt="RightArrow"/>
                </div>
            </button>

            {/*{isDropdownOpen && (*/}
            <div
                className={`absolute right-1 z-10 top-0 pt-14 w-64 bg-white rounded-xl shadow-profile-popup-shadow px-4 py-2 transform transition-all duration-100 ${isDropdownOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0 hidden'} origin-top`}
            >
                <div className="h-1"/>
                <HorizontalSeparator paddingY="my-1" height="h-[1px]" color="bg-[#F6F6F6]"/>
                <div className="h-1"/>
                <DropdownMenuButton icon={UserIcon} label="My Profile" onClick={() => {
                }}/>
                <DropdownMenuButton icon={ChangePasswordIcon} label="Change Password"
                                    onClick={() => openPopup(<PasswordResetPopup/>)}/>
                <DropdownMenuButton icon={HelpIcon} label="Help" onClick={() => {
                }}/>
                <div className="h-1"/>
                <HorizontalSeparator paddingY="" height="h-[1px]" color="bg-[#F6F6F6]"/>
                <div className="h-1"/>
                <DropdownMenuButton icon={LogoutIcon} label="Sign Out" onClick={handleLogout}/>
            </div>
            {/*)}*/}

        </div>


    </div>
  );
};

export default ProfileBar;
