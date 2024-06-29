import GuidelinePage from "../../pages/GuidelinePage";
import React from "react";
import HiwiHomePage from "../../pages/home-page/HiwiHomePage";
import ContractPage from "../../pages/ContractPage";
import SupervisorHomePage from "../../pages/home-page/SupervisorHomePage";
import AnalysisPage from "../../pages/AnalysisPage";
import EmployeesPage from "../../pages/EmployeesPage";
import DocumentPage from "../../pages/document-page/DocumentPage";
import AdminHomePage from "../../pages/home-page/AdminHomePage";
import HiwiAnalysisPage from "../../pages/analysis-page/HiwiAnalysisPage";
import SupervisorAnalysisPage from "../../pages/analysis-page/SupervisorAnalysisPage";
import ProjectsPage from "../../pages/ProjectsPage";
import SecretaryDocumentPage from "../../pages/document-page/SecretaryDocumentPage";
import SupervisorEmployeesPage from "../../pages/employees/SupervisorEmployeesPage";
import SecretaryEmployeesPage from "../../pages/employees/SecretaryEmployeesPage";
import AdminAnalysisPage from "../../pages/analysis-page/AdminAnalysisPage";

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
    "/analysis": HiwiAnalysisPage,
    "/documents": DocumentPage,
    "/contract": ContractPage
  },
  Supervisor: {
    ...commonRoutes,
    "/home": SupervisorHomePage,
    "/analysis": SupervisorAnalysisPage,
    "/employees": SupervisorEmployeesPage,
    "/projects": ProjectsPage,
  },
  Secretary: {
    ...commonRoutes,
    "/home": SupervisorHomePage,
    "/analysis": SupervisorAnalysisPage,
    "/documents": SecretaryDocumentPage,
    "/employees": SecretaryEmployeesPage,
  },
  Admin: {
    ...commonRoutes,
    "/home": AdminHomePage,
    "/analysis": AdminAnalysisPage,
  }
};