import React from 'react';
import {useAuth} from "../../context/AuthContext";
import {RoleDocumentsPageMap, Roles} from "../../components/auth/roles";

const DocumentRoleMapping: React.FC = () => {
  const { role } = useAuth();

  const DocumentPageComponent = RoleDocumentsPageMap[role as Roles];

  if (!DocumentPageComponent) {
    return <div>Unauthorized</div>;
  }

  return <DocumentPageComponent/>;
};

export default DocumentRoleMapping;