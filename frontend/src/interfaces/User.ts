import { PersonalInfo } from './PersonalInfo';
import {ContractInfo} from "./ContractInfo";

export interface User {
  _id: string;
  username: string;
  role: string;
  profileImageUrl?: string;
  personalInfo: PersonalInfo;
  timesheets?: string[];
  contractInfo?: ContractInfo;
  accountCreation?: string;
  lastLogin?: string;
  supervisor?: string;
}
