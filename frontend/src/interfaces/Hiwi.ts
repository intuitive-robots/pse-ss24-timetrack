import { PersonalInfo } from './PersonalInfo';

export interface User {
  _id: string;
  username: string;
  role: string;
  profileImageUrl: string;
  personalInfo: PersonalInfo;
}
