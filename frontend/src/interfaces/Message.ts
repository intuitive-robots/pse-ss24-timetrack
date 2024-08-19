export interface NotificationMessage {
  _id: string;
  receiver: string;
  sender: string;
  message: string;
  messageType: string;
  timestamp: string;
  read: boolean;
  sent: boolean;
  messageData: any;
}
