import GuidelinePage from "../../pages/GuidelinePage";
import React from "react";
import HiwiHomePage from "../../pages/home-page/HiwiHomePage";
import DocumentRoleMapping from "../../pages/document-page/DocumentRoleMapping";
import ContractPage from "../../pages/ContractPage";
import SupervisorHomePage from "../../pages/home-page/SupervisorHomePage";
import AnalysisPage from "../../pages/AnalysisPage";
import EmployeesPage from "../../pages/EmployeesPage";
import DocumentPage from "../../pages/document-page/DocumentPage";
import AdminHomePage from "../../pages/home-page/AdminHomePage";

const commonRoutes = {
    "/guidelines": GuidelinePage,
};

interface RoutesConfig {
  [role: string]: {
    [path: string]: React.ComponentType<any>;
  };
}

export const routesConfig: RoutesConfig  = {
  Hiwi: {
    ...commonRoutes,
    "/home": HiwiHomePage,
    "/documents": DocumentRoleMapping,
    "/contract": ContractPage,
  },
  Supervisor: {
    ...commonRoutes,
    "/home": SupervisorHomePage,
    "/analysis": AnalysisPage,
    "/employees": EmployeesPage,
    "/documents": DocumentPage,
  },
  Admin: {
    ...commonRoutes,
    "/home": AdminHomePage,
    "/analysis": AnalysisPage,
    "/documents": DocumentPage,
  }
};