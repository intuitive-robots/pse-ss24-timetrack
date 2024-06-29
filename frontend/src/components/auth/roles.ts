import AdminHomePage from "../../pages/home-page/AdminHomePage";
import SupervisorHomePage from "../../pages/home-page/SupervisorHomePage";
import SecretaryHomePage from "../../pages/home-page/SecretaryHomePage";
import HiwiHomePage from "../../pages/home-page/HiwiHomePage";

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
