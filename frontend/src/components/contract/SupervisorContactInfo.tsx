import React, { useState, useEffect } from 'react';
import { getHiwiSupervisor } from '../../services/UserService';
import UserInfo from "../UserInfo";
import MailIcon from "../../assets/images/contact_mail.svg";
import SlackIcon from "../../assets/images/contact_slack.svg";
import ProfilePicture from "../../assets/images/profile_placeholder.svg";
import ContactButton from "../input/ContactButton";
import {Roles} from "../auth/roles";

const UserContactInfo: React.FC = () => {
    const [supervisor, setSupervisor] = useState<any | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [message, setMessage] = useState('');

    useEffect(() => {
        getHiwiSupervisor().then(data => {
            setSupervisor(data);
        }).catch(error => {
            console.error('Failed to fetch supervisor:', error);
            alert('Failed to fetch supervisor data.');
        }).finally(() => setIsLoading(false));
    }, []);

    const handleCopyEmail = async () => {
        if (supervisor && supervisor.email) {
            try {
                await navigator.clipboard.writeText(supervisor.email);
                setMessage(`${supervisor.email} copied to clipboard `);
                setTimeout(() => setMessage(''), 2000);
            } catch (err) {
                setMessage('Failed to copy email.');
                setTimeout(() => setMessage(''), 2000);
            }
        }
    };

    const handleCopySlack = async () => {
        if (supervisor && supervisor.email) {
            try {
                setMessage(`Slack is coming soon to Clockwise.`);
                setTimeout(() => setMessage(''), 2000);
            } catch (err) {
                setMessage('Failed to copy slack.');
                setTimeout(() => setMessage(''), 2000);
            }
        }
    };


    return (
        <div className="flex flex-col items-center">
            <div className="flex flex-row justify-between w-full">
                <UserInfo
                    name={isLoading ? "" : supervisor.firstName}
                    lastName={isLoading ? "" : supervisor.lastName}
                    role={isLoading ? Roles.Supervisor : (supervisor.role || "N/A")}
                    profileImageUrl={isLoading ? ProfilePicture : (supervisor.profileImageUrl || ProfilePicture)}
                    loading={isLoading}
                />
                <div className="flex flex-row gap-3">
                    <ContactButton icon={MailIcon} onClick={handleCopyEmail}/>
                    <ContactButton icon={SlackIcon} onClick={handleCopySlack}/>
                </div>
            </div>
            {message &&
                <div className="fixed bottom-0 left-0 right-0 bg-purple-500 text-white font-bold text-center py-2.5">{message}</div>}
        </div>
    );
};

export default UserContactInfo;
