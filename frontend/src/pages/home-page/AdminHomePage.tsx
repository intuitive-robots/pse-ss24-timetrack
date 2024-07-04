import React, {useEffect, useState} from 'react';
import UserCard from "../../components/UserCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.svg"
import {getUsers} from "../../services/AuthService";
import {User} from "../../interfaces/User";
import {useAuth} from "../../context/AuthContext";

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
        <div className="px-6 py-6">
            <p className="text-lg font-medium text-subtitle">{user ? user.personalInfo.instituteName : "Institute of Intuitive Robotic"}</p>
            <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello {user ? user.personalInfo.firstName : ""},</h1>
            <h2 className="text-md font-medium text-subtitle mt-1">There are {users.length} employees, including {hiwiCount} HiWis
                and {supervisorCount} supervisors</h2>
            <div className="flex-grow py-6 overflow-y-auto mb-60">
                {users.map(user => (
                    <UserCard
                        key={user.username}
                        name={user.personalInfo.firstName}
                        lastName={user.personalInfo.lastName}
                        role={user.role}
                        profileImageUrl={ProfilePlaceholder}
                        onView={() => {
                        }}
                        onEdit={() => {
                        }}
                        onDelete={() => {
                        }}
                    />
                ))}
            </div>
        </div>
    );
};

export default AdminHomePage;
