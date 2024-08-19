import React from 'react';
import {roleColors} from "../utils/RoleMapping";
import DynamicProfilePicture from "./profile/DynamicProfilePicture";

interface UserInfoSecretaryProps {
    firstName: string;
    lastName: string;
    supervisor: string;
}

/**
 * UserInfoSupervisorView component to display user profile information.
 *
 * @component
 * @param {UserInfoSecretaryProps} props - The props passed to the UserInfoSupervisorView component.
 * @returns {React.ReactElement} A React Element that renders the user's profile information.
 */
const UserInfoSecretaryView: React.FC<UserInfoSecretaryProps> = ({
                                                                     firstName,
                                                                     lastName,
                                                                     supervisor,
                                                                 }: UserInfoSecretaryProps): React.ReactElement => {
    return (
        <div className="flex items-center space-x-3 z-50 py-1">
            <DynamicProfilePicture firstName={firstName} lastName={lastName} size={45}/>
            <div className="flex flex-col items-start">
                <p className="text-card-title text-md font-semibold">{`${firstName} ${lastName}`}</p>
                <p className={`text-sm text-accent] font-medium ${roleColors["Supervisor"]}`}>Supervisor: {supervisor}</p>
            </div>
        </div>
    );
};

export default UserInfoSecretaryView;
