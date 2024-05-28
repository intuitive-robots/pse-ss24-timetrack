import React from 'react';
import LayoutWrapper from "../components/LayoutWrapper";

/**
 * HomePage component serves as the main landing page for the application.
 *
 * @returns {React.ReactElement} A React Element that renders the main homepage of the application.
 */
const HomePage = (): React.ReactElement => {
    return (
        <LayoutWrapper
            pageContent={<div>Page Content</div>} // Embeds static page content inside the layout wrapper
        />
    );
};

export default HomePage;
