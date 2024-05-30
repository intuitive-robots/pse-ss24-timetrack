import React from "react";

/**
 * NotFound component that renders a simple message indicating that the page was not found.
 *
 * @component
 * @returns {React.ReactElement} A React Element that renders a 404 not found message.
 */
const NotFound: React.FC = (): React.ReactElement => {
  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-4xl font-bold">404 Not Found</h1>
    </div>
  );
}

export default NotFound;