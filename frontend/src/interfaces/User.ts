import { PersonalInfo } from './PersonalInfo';
import { EmploymentDetails } from './EmploymentDetails';

export interface User {
  _id: string;
  username: string;
  role: string;
  profileImageUrl: string;
  personalInfo: PersonalInfo;
  employmentDetails: EmploymentDetails;
}
