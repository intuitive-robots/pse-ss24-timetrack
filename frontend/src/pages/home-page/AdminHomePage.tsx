import React, { useEffect, useState } from 'react';
import UserCard from "../../components/UserCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import { getUsers } from "../../services/AuthService";
import { User } from "../../interfaces/User";
import { useAuth } from "../../context/AuthContext";
import ConfirmationPopup from "../../components/popup/ConfirmationPopup";
import { usePopup } from "../../components/popup/PopupContext";
import { deleteUser } from "../../services/UserService";
import RoleFilter from "../../components/filter/RoleFilter";
import {getPluralForm} from "../../utils/TextUtils";
import EditUserPopup from "../../components/popup/EditUserPopup";
import ViewUserPopup from "../../components/popup/ViewUserPopup";

interface RoleCounts {
    Hiwi: number;
    Supervisor: number;
    Secretary: number;
    Admin: number;
}

const AdminHomePage = (): React.ReactElement => {
    const { user } = useAuth();
    const [users, setUsers] = useState<User[]>([]);
    const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
    const [activeRole, setActiveRole] = useState<string>("View all");

    const { openPopup, closePopup } = usePopup();

    const handleDeleteUser = (username: string) => {
        openPopup(
            <ConfirmationPopup
                title={"Delete User"}
                description={"Are you sure you want to delete this user including user data?"}
                note={"NOTE: This action cannot be undone."}
                noteColor={"text-red-600"}
                onConfirm={() => confirmDeleteUser(username)}
                onCancel={closePopup}
            />
        );
    };

    const handleLockUser = (username: string) => {
        openPopup(
            <ConfirmationPopup
                title={"Lock User"}
                description={"Are you sure you want to lock this user?"}
                note={"NOTE: This action will not remove any user data"}
                onConfirm={() => confirmLockUser(username)}
                onCancel={closePopup}
            />
        );
    };

    const confirmDeleteUser = async (username: string) => {
        try {
            await deleteUser(username);
            closePopup();
            setUsers(prev => prev.filter(u => u.username !== username));
        } catch (error) {
            console.error('Failed to delete user:', error);
            closePopup();
        }
    };

    const confirmLockUser = async (username: string) => {
        try {
            closePopup();
        } catch (error) {
            console.error('Failed to Lock user:', error);
            closePopup();
        }
    };

    const fetchUsers = async () => {
        try {
            const fetchedUsers = await getUsers();
            setUsers(fetchedUsers);
            setFilteredUsers(fetchedUsers);
        } catch (error) {
            console.error('Failed to fetch users', error);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    useEffect(() => {
        if (activeRole === "View all") {
            setFilteredUsers(users.filter(user => !user.username.startsWith('test')));
        } else {
            setFilteredUsers(users.filter(user => user.role === activeRole && !user.username.startsWith('test')));
        }
    }, [activeRole, users]);

    const handleOnChange = (user: User) => {
        openPopup(<EditUserPopup userData={user}/>, fetchUsers);
    }

    const generateHeader = () => {
        if (activeRole === "View all") {
            const initialCounts: RoleCounts = { Hiwi: 0, Supervisor: 0, Secretary: 0, Admin: 0 };
            const roleCounts = users.reduce((acc, user) => {
                if (user.role in acc) {
                    acc[user.role as keyof RoleCounts]++;
                }
                return acc;
            }, initialCounts);

            const totalEmployees = filteredUsers.length;
            const employeeNoun = getPluralForm(totalEmployees, 'employee', 'employees');
            const verb = totalEmployees === 1 ? 'is' : 'are';

            return `There ${verb} ${totalEmployees} ${employeeNoun}, including ${roleCounts.Hiwi} HiWi${roleCounts.Hiwi === 1 ? '' : 's'}, ${roleCounts.Supervisor} Supervisor${roleCounts.Supervisor === 1 ? '' : 's'}, ${roleCounts.Secretary} Secretary${roleCounts.Secretary === 1 ? '' : 's'}, and ${roleCounts.Admin} Admin${roleCounts.Admin === 1 ? '' : 's'}.`;
        } else {
            const count = filteredUsers.length;
            const roleNoun = getPluralForm(count, activeRole, activeRole + 's');
            const verb = count === 1 ? 'is' : 'are';

            return `There ${verb} ${count} ${roleNoun}.`;
        }
    };

    return (
        <div className="flex flex-col h-full px-6 mt-6">
            <div className="mb-4">
                <p className={`text-lg font-medium text-subtitle transition-all duration-300 ease-in-out ${!user ? 'blur-sm' : 'blur-none'}`}>
                    {user ? user.personalInfo.instituteName : "Institute Name"}
                </p>
                <h1 className="text-3xl font-bold text-headline mt-4">
                    Hello <span className={`transition-all duration-300 ease-in-out ${user ? 'blur-none' : 'blur-sm'}`}>
                    {user ? user.personalInfo.firstName : 'IRL'}
                </span>,
                </h1>
                <h2 className={`text-md font-medium text-subtitle mt-1 transition-all duration-300 ease-in-out ${users? 'blur-none' : 'blur-sm'}`}>
                    {generateHeader()}
                </h2>
                <RoleFilter onRoleChange={setActiveRole}/>
            </div>
            <div className="flex flex-col overflow-y-auto gap-0 mb-6 mt-2 flex-grow">
                {filteredUsers.map((user) => (
                    <UserCard
                        key={user.username}
                        username={user.username}
                        name={user.personalInfo.firstName}
                        lastName={user.personalInfo.lastName}
                        role={user.role}
                        profileImageUrl={ProfilePlaceholder}
                        onView={() => {openPopup(<ViewUserPopup userData={user}/>)}}
                        onEdit={() => {handleOnChange(user)}}
                        onLock={() => {handleLockUser(user.username)}}
                        onDelete={() => handleDeleteUser(user.username)}
                    />
                ))}
            </div>
        </div>
    );
};

export default AdminHomePage;
