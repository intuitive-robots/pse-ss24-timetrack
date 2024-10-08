import React, {useEffect, useState} from 'react';
import UserCard from "../../components/UserCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg";
import {getUsers} from "../../services/AuthService";
import {User} from "../../interfaces/User";
import {useAuth} from "../../context/AuthContext";
import ConfirmationPopup from "../../components/popup/ConfirmationPopup";
import {usePopup} from "../../components/popup/PopupContext";
import {archiveUser, getArchivedUsers, activateUser, deleteUser} from "../../services/UserService";
import RoleFilter from "../../components/filter/RoleFilter";
import {getPluralForm} from "../../utils/TextUtils";
import EditUserPopup from "../../components/popup/EditUserPopup";
import ViewUserPopup from "../../components/popup/ViewUserPopup";
import {useSearch} from "../../context/SearchContext";
import {SearchUtils} from "../../utils/SearchUtils";

interface RoleCounts {
    Hiwi: number;
    Supervisor: number;
    Secretary: number;
    Admin: number;
}

const AdminHomePage = (): React.ReactElement => {
    let { user } = useAuth();
    const { searchString } = useSearch();
    const { openPopup, closePopup } = usePopup();

    const [users, setUsers] = useState<User[]>([]);
    const [archivedUsers, setArchivedUsers] = useState<User[]>([]);
    const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
    const [activeRole, setActiveRole] = useState<string>("View all");
    const [searchUtils, setSearchUtils] = useState<SearchUtils<User> | null>(null);

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

    const handleArchiveUser = (username: string) => {
        openPopup(
            <ConfirmationPopup
                title={"Archive User"}
                description={"Are you sure you want to lock this user?"}
                note={"NOTE: This action will not remove any user data"}
                onConfirm={() => confirmArchiveUser(username)}
                onCancel={closePopup}
            />
        );
    };

    const handleActivateUser = (username: string) => {
        openPopup(
            <ConfirmationPopup
                title={"Activate User"}
                description={"Are you sure you want to activate this user?"}
                note={"NOTE: This action will not remove any user data"}
                onConfirm={() => confirmActivateUser(username)}
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

    const confirmArchiveUser = async (username: string) => {
        try {
            await archiveUser(username);
            closePopup();
            fetchUsers();
            fetchArchivedUsers();
        } catch (error) {
            alert(`Failed to Archive user ${error}`);
            closePopup();
        }
    };

    const confirmActivateUser = async (username: string) => {
        try {
            await activateUser(username);
            closePopup();
            fetchUsers();
            fetchArchivedUsers();
        } catch (error) {
            alert(`Failed to Activate user ${error}`);
            closePopup();
        }
    };

    const fetchUsers = async () => {
        try {
            const fetchedUsers = await getUsers();
            setUsers(fetchedUsers);
            setSearchUtils(new SearchUtils(fetchedUsers, {
                keys: ["role", "username", "personalInfo.firstName", "personalInfo.lastName"],
                threshold: 0.3
            }));
        } catch (error) {
            console.error('Failed to fetch users', error);
        }
    };

    const fetchArchivedUsers = async () => {
        try {
            const fetchedArchivedUsers = await getArchivedUsers();
            setArchivedUsers(fetchedArchivedUsers);
        } catch (error) {
            console.error('Failed to fetch users', error);
        }
    };

    useEffect(() => {
        fetchUsers();
        fetchArchivedUsers();
    }, []);

    useEffect(() => {
        const results = searchUtils && searchString ? searchUtils.searchItems(searchString) : users;
        const filteredByRole = activeRole === "View all" ? results : results.filter(user => user.role === activeRole);
        const nonTestUsers = filteredByRole.filter(user => !user.username.startsWith('test'));
        setFilteredUsers(nonTestUsers);
    }, [searchString, searchUtils, users, activeRole]);

    useEffect(() => {
        if (activeRole === "View all") {
            setFilteredUsers(users.filter(user => !user.username.startsWith('test') && !user.isArchived));
        } else if (activeRole === "Archived") {
            setFilteredUsers(archivedUsers);
        } else {
            setFilteredUsers(users.filter(user => user.role === activeRole && !user.username.startsWith('test') && !user.isArchived));
        }
    }, [activeRole, users, archivedUsers]);

    const handleOnChange = (user: User) => {
        openPopup(<EditUserPopup userData={user}/>, fetchUsers);
    }

    const generateHeader = () => {
        if (activeRole === "View all") {
            const initialCounts: RoleCounts = { Hiwi: 0, Supervisor: 0, Secretary: 0, Admin: 0};
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
                        isArchived={user.isArchived}
                        onView={() => {openPopup(<ViewUserPopup userData={user}/>)}}
                        onEdit={() => {handleOnChange(user)}}
                        onArchive={() => {handleArchiveUser(user.username)}}
                        onActivate={() => {handleActivateUser(user.username)}}
                        onDelete={() => handleDeleteUser(user.username)}
                    />
                ))}
            </div>
        </div>
    );
};

export default AdminHomePage;
