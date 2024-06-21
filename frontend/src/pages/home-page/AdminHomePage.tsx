import React, {useEffect, useState} from 'react';
import LayoutWrapper from "../../components/LayoutWrapper";
import UserCard from "../../components/UserCard";
import ProfilePlaceholder from "../../assets/images/profile_placeholder.png"
import {getUsers} from "../../services/AuthService";
import {User} from "../../interfaces/User";

/**
 * AdminHomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const AdminHomePage = (): React.ReactElement => {
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
    const fetchUsers = async () => {
      try {
        const users = await getUsers();
        console.log('Fetched users:', users); // Log fetched users
        setUsers(users);
      } catch (error) {
        console.log('Failed to fetch users');
      }
    };

    fetchUsers();
  }, []);

    return (
        <LayoutWrapper
            pageContent={
                <div className="px-6 py-6">
                    <p className="text-lg font-medium text-subtitle">Institute for Intuitive Robotics</p>
                    <h1 className="text-3xl font-bold text-gray-800 mt-5">Hello Nico,</h1>
                    <h2 className="text-md font-medium text-subtitle mt-1">There are {users.length} employees, including * HiWis and
                        * supervisors</h2>
                    <div className="h-5"/>
                    <div>
                        {users.map(user => (
                            <UserCard
                                key={user._id}
                                name={user.personalInfo.firstName}
                                lastName={user.personalInfo.lastName}
                                role={user.role}
                                profileImageUrl={ProfilePlaceholder}
                                onView={() => {}}
                                onEdit={() => {}}
                                onDelete={() => {}}
                            />
                        ))}
                    </div>
                </div>
            }
        />
    );
};

export default AdminHomePage;
