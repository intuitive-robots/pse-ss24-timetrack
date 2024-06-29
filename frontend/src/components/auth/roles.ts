import AdminHomePage from "../../pages/home-page/AdminHomePage";
import SupervisorHomePage from "../../pages/home-page/SupervisorHomePage";
import SecretaryHomePage from "../../pages/home-page/SecretaryHomePage";
import HiwiHomePage from "../../pages/home-page/HiwiHomePage";
import DocumentsPage from "../../pages/document-page/DocumentPage";
import DocumentRoleMapping from "../../pages/document-page/DocumentRoleMapping";
import GuidelinePage from "../../pages/GuidelinePage";
import ContractPage from "../../pages/ContractPage";
import HomePage from "../../pages/home-page/HomePage";
import EmployeesPage from "../../pages/EmployeesPage";
import AnalysisPage from "../../pages/AnalysisPage";
import DocumentPage from "../../pages/document-page/DocumentPage";
import React from "react";

export enum Roles {
  Hiwi = 'Hiwi',
  Supervisor = 'Supervisor',
  Secretary = 'Secretary',
  Admin = 'Admin',
}

export const RoleHomePageMap = {
  [Roles.Hiwi]: HiwiHomePage,
  [Roles.Supervisor]: SupervisorHomePage,
  [Roles.Secretary]: SecretaryHomePage,
  [Roles.Admin]: AdminHomePage,
};

export const RoleDocumentsPageMap = {
  [Roles.Hiwi]: DocumentsPage,
  [Roles.Supervisor]: DocumentsPage,
  [Roles.Secretary]: DocumentsPage,
  [Roles.Admin]: DocumentsPage,
};


