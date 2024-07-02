import HomeIcon from '../../assets/images/navbar/home.svg';
import HomeIconActive from '../../assets/images/navbar/home_active.svg';
import DocumentsIcon from '../../assets/images/navbar/documents.svg';
import DocumentsIconActive from '../../assets/images/navbar/documents_active.svg';
import AnalysisIcon from '../../assets/images/navbar/analysis.svg';
import AnalysisIconActive from '../../assets/images/navbar/analysis_active.svg';
import ContractIcon from '../../assets/images/navbar/contract.svg';
import ContractIconActive from '../../assets/images/navbar/contract_active.svg';
import GuidelinesIcon from '../../assets/images/navbar/guidelines.svg';
import GuidelinesIconActive from '../../assets/images/navbar/guidelines_active.svg';
import ProjectsIcon from '../../assets/images/navbar/projects.svg';
import ProjectsIconActive from '../../assets/images/navbar/projects_active.svg';
import EmployeesIcon from '../../assets/images/navbar/employees.svg';
import EmployeesIconActive from '../../assets/images/navbar/employees_active.svg';

interface IconPair {
  default: string;
  active: string;
}

interface NavigationIcons {
  [key: string]: IconPair;
}

const navigationIcons: NavigationIcons = {
  Home: { default: HomeIcon, active: HomeIconActive },
  Analysis: { default: AnalysisIcon, active: AnalysisIconActive },
  Documents: { default: DocumentsIcon, active: DocumentsIconActive },
  Contract: { default: ContractIcon, active: ContractIconActive },
  Guidelines: { default: GuidelinesIcon, active: GuidelinesIconActive },
  AssignedEmployees: {default: EmployeesIcon, active: EmployeesIconActive },
  Projects: {default: ProjectsIcon, active: ProjectsIconActive },
  Employees: {default: EmployeesIcon, active: EmployeesIconActive },
};

export default navigationIcons;