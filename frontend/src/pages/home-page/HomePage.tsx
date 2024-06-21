import React from 'react';
import {useAuth} from "../../context/AuthContext";
import {RoleHomePageMap, Roles} from "../../components/auth/roles";

const HomePage: React.FC = () => {
  const { role } = useAuth();

  const HomePageComponent = RoleHomePageMap[role as Roles];

  if (!HomePageComponent) {
    return <div>Unauthorized</div>;
  }

  return <HomePageComponent/>;
};

export default HomePage;