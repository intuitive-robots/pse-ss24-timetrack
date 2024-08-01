import React from 'react';
import NotificationItem from './NotificationItem';
import {Message} from "../../interfaces/Message";
import HorizontalSeparator from "../../shared/HorizontalSeparator";

const NotificationsList: React.FC = () => {
    const notifications: Message[] = [
        {
            receiver: 'Simon',
            sender: 'Marco Ruth',
            message: 'break time 16th should be 30 minutes.',
            messageType: 'Change Request',
            creationDate: new Date('2022-07-16')
        },
        {
            receiver: 'Simon',
            sender: 'Marco Ruth',
            message: 'The submission perio ends in 3 days.',
            messageType: 'Reminder',
            creationDate: new Date('2022-07-16')
        },
        {
            receiver: 'Simon',
            sender: 'Marco Ruth',
            message: 'break time 16th should be 30 minutes.',
            messageType: 'Reminder',
            creationDate: new Date('2022-07-16')
        }
    ];

    return (
        <div>
            {notifications.map((notification: Message, index) => (
                <div>
                    <NotificationItem
                        key={index}
                        notification={notification}
                    />
                    <HorizontalSeparator/>
                </div>
            ))}
        </div>
    );
};

export default NotificationsList;
