import React, {useEffect, useState} from 'react';
import UserCard from "../../components/UserCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg"
import {getUsers} from "../../services/AuthService";
import {User} from "../../interfaces/User";
import {useAuth} from "../../context/AuthContext";
import ConfirmationPopup from "../../components/popup/ConfirmationPopup";
import {deleteTimeEntry} from "../../services/TimeEntryService";
import {usePopup} from "../../components/popup/PopupContext";
import {deleteUser} from "../../services/UserService";

/**
 * AdminHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const AdminHomePage = (): React.ReactElement => {
    const {user} = useAuth();
    const [users, setUsers] = useState<User[]>([]);

    const [hiwiCount, setHiwiCount] = useState(0);
    const [supervisorCount, setSupervisorCount] = useState(0);

    const { openPopup, closePopup } = usePopup();

     const handleDeleteUser = (username: string) => {
        openPopup(
          <ConfirmationPopup
            onConfirm={() => confirmDeleteUser(username)}
            onCancel={closePopup}
          />
        );
     };

     const confirmDeleteUser = async (username: string) => {
        try {
            await deleteUser(username);
            closePopup();
        } catch (error) {
            console.error('Failed to delete user:', error);
            closePopup();
        }
     };

    useEffect(() => {
        const fetchUsers = async () => {
          try {
            const fetchedUsers: User[] = await getUsers();
            setUsers(fetchedUsers);

            const hiwiCount = fetchedUsers.filter(user => user.role === "Hiwi").length;
            const supervisorCount = fetchedUsers.filter(user => user.role === "Supervisor").length;

            setHiwiCount(hiwiCount);
            setSupervisorCount(supervisorCount);
          } catch (error) {
            console.log('Failed to fetch users');
          }
        };

        fetchUsers();
    }, []);

    return (
        <div className="flex flex-col h-full px-6 mt-6">
            <div className="mb-4">
                <p className="text-lg font-medium text-subtitle">{user ? user.personalInfo.instituteName : "Institute Name"}</p>
                <h1 className="text-3xl font-bold text-gray-800 mt-3.5">Hello {user ? user.personalInfo.firstName : "User"}</h1>
                <h2 className="text-md font-medium text-subtitle mt-1">There are {users.length} employees, including {hiwiCount} HiWis and {supervisorCount} supervisors</h2>
            </div>
            <div className="flex flex-col overflow-y-auto mb-6 mt-2 flex-grow">
                {users.map(user => (
                    <UserCard
                        key={user.username}
                        name={user.personalInfo.firstName}
                        lastName={user.personalInfo.lastName}
                        role={user.role}
                        profileImageUrl={ProfilePlaceholder}
                        onView={() => {}}
                        onEdit={() => {}}
                        onDelete={() => {handleDeleteUser(user.username)}}
                    />
                ))}
            </div>
        </div>
    );
};

export default AdminHomePage;
