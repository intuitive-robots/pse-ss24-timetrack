import React from 'react';
import NavigationBar from './navbar/NavigationBar';
import ProfileBar from './ProfileBar';
import ProfilePlaceholder from "../assets/images/profile_placeholder.png";

interface LayoutWrapperProps {
  pageContent: React.ReactNode;
}

/**
 * The LayoutWrapper component is responsible for providing the overall page layout.
 * It includes a profile bar at the top, a navigation bar on the left, and a dynamic content area that renders `pageContent`.
 *
 * @param {LayoutWrapperProps} props - The props passed to the component.
 * @returns {React.ReactElement} The rendered component.
 */
const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ pageContent }: LayoutWrapperProps): React.ReactElement => {
  return (
    <div className="flex flex-col min-h-screen select-none">
      {/* Full-width profile bar at the top of the page */}
      <div className="w-full">
        <ProfileBar
          name="Nico Maier"
          role="Hilfswissenschaftler"
          imageUrl={ProfilePlaceholder}
        />
      </div>
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar navigation bar */}
        <div className="">
          <NavigationBar />
        </div>
        {/* Main content area that takes remaining space */}
        <div className="flex-1 overflow-auto p-4 items-start justify-start">
          {pageContent}
        </div>
      </div>
    </div>
  );
};

export default LayoutWrapper;