import React from 'react';
import { useAuth } from "../../context/AuthContext";
import UserInfoSupervisorView from "../UserInfoSupervisorView";
import MailIcon from "../../assets/images/contact_mail.svg";
import SlackIcon from "../../assets/images/contact_slack.svg";
import ProfilePicture from "../../assets/images/profile_placeholder.svg";
import ContactButton from "../input/ContactButton";

interface UserContactInfoProps {
  username: string;
}

const UserContactInfo: React.FC<UserContactInfoProps> = ({ username }) => {
  const { user } = useAuth();

  if (!user || user.username !== username) {
    return null;
  }

  return (
    <div className="flex flex-row justify-between">
      <UserInfoSupervisorView
        name={user.personalInfo.firstName}
        lastName={user.personalInfo.lastName}
        role={user.role || "N/A"}
        profileImageUrl={user.profileImageUrl || ProfilePicture}
      />
      <div className="flex flex-row gap-3">
        <ContactButton icon={MailIcon} onClick={() => console.log('Send Mail')} />
        <ContactButton icon={SlackIcon} onClick={() => console.log('Send Slack Message')} />
      </div>
    </div>
  );
};

export default UserContactInfo;
