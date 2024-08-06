import {ReactNode} from "react";
import {HomeIcon} from "../../assets/iconComponents/navbar/HomeIcon";
import React from 'react';
import {AnalysisIcon} from "../../assets/iconComponents/navbar/AnalysisIcon";
import {ContractIcon} from "../../assets/iconComponents/navbar/ContractIcon";
import {GuidelinesIcon} from "../../assets/iconComponents/navbar/GuidelinesIcon";
import {DocumentsIcon} from "../../assets/iconComponents/navbar/DocumentsIcon";
import {ProjectsIcon} from "../../assets/iconComponents/navbar/ProjectsIcon";
import {EmployeesIcon} from "../../assets/iconComponents/navbar/EmployeesIcon";

interface IconPair {
  default: string | ReactNode;
  active: string | ReactNode;
}

interface NavigationIcons {
  [key: string]: IconPair;
}

const navigationIcons: NavigationIcons = {
  Home: { default: <HomeIcon isActive={false}/>, active: <HomeIcon isActive={true}/> },
  Analysis: { default: <AnalysisIcon isActive={false}/>, active: <AnalysisIcon isActive={true}/>},
  Documents: { default: <DocumentsIcon isActive={false}/>, active: <DocumentsIcon isActive={true}/> },
  Contract: { default: <ContractIcon isActive={false}/>, active: <ContractIcon isActive={true}/>},
  Guidelines: { default: <GuidelinesIcon isActive={false}/>, active: <GuidelinesIcon isActive={true}/> },
  AssignedEmployees: {default: <EmployeesIcon isActive={false}/>, active: <EmployeesIcon isActive={true}/> },
  Projects: {default: <ProjectsIcon isActive={false}/>, active: <ProjectsIcon isActive={true}/> },
  Employees: {default: <EmployeesIcon isActive={false}/>, active: <EmployeesIcon isActive={true}/> },
};

export default navigationIcons;