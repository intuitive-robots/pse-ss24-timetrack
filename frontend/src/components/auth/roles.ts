import AdminHomePage from "../../pages/home-page/AdminHomePage";
import SupervisorHomePage from "../../pages/home-page/SupervisorHomePage";
import SecretaryHomePage from "../../pages/home-page/SecretaryHomePage";
import HiwiHomePage from "../../pages/home-page/HiwiHomePage";
import DocumentsPage from "../../pages/document-page/DocumentPage";
import DocumentRoleMapping from "../../pages/document-page/DocumentRoleMapping";

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
