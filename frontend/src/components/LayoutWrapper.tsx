import React from 'react';
import NavigationBar from './navbar/NavigationBar';
import ProfileBar from './ProfileBar';
import ProfilePlaceholder from "../assets/images/profile_placeholder.png";

interface LayoutWrapperProps {
  pageContent: React.ReactNode;
}

const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ pageContent }) => {
  return (
    <div className="flex flex-col min-h-screen select-none">
      <div className="w-full">
        <ProfileBar
            name="Nico Maier"
            role="Hilfswissenschaftler"
            imageUrl={ProfilePlaceholder}
        />
      </div>
      <div className="flex flex-1 overflow-hidden">
        <div className=""> {/* Navigationbar below Profilebar*/}
          <NavigationBar />
        </div>
        <div className="flex-1 overflow-auto p-4 items-start justify-start">
          {pageContent}
        </div>
      </div>
    </div>
  );
};

export default LayoutWrapper;
