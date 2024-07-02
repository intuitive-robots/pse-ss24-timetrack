import React from 'react';

interface ContactButtonProps {
  icon: string;
  onClick: () => void;
}

const ContactButton: React.FC<ContactButtonProps> = ({ icon, onClick }) => {
  return (
    <button
      className="p-3.5 bg-purple-200 rounded-full hover:bg-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-300"
      onClick={onClick}
      aria-label="Contact Us"
    >
      <img src={icon} alt="Contact"/>
    </button>
  );
};

export default ContactButton;