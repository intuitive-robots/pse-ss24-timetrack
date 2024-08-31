# Intuitive Time Tracking Web-App for Research Assistants

## Project Overview

This repository contains the code for a web application designed to simplify and streamline the process of time tracking for research assistants (HiWis) at Intuitive Robots Lab. The application facilitates accurate recording of work hours and ensures compliance with institutional regulations.

## Features

- **Time Entry**: Users can log their daily work hours, including start and end times, and break durations.
- **Vacation Management**: Users can take vacation hours, view vacation entries, and track their remaining vacation entitlement. The available vacation hours for Hiwis are automatically calculated based on their contract data.
- **Signature Verification**: At the end of each month, users can sign their timesheets electronically, making them ready for supervisor review. Signature validation ensures that signing is only possible after completing at least 80% of the contractual work hours and signatures are registered within system.
- **User Profile Management**: Users can change their password, and manage their login credentials.
- **Contract Overview**: Displays detailed contract information including assigned weekly work hours, team details, hourly rate, and supervisor contact information.
- **Document View**: Hiwis have access to a document view where they can review all their timesheets and download them as PDFs once they are fully signed.
- **Digital Signature Upload**: Users can upload a digital image of their signature for use in official documents and timesheet verification.
- **Comprehensive Time Entry Validation**: Time Entries undergo extensive validation using multiple strategies. This includes format input validation, checks for weekends or holidays, ensuring that regular working hours are not exceeded by more than 2 hours, and verifying that break times are adhered to.
- **Notification Integration** In-app notifications inform users of important updates, such as status changes and deadlines.
- **Slack Integration:** Integrates with the Slack API to provide additional notifications to users via Slack, reminding them of status changes or upcoming deadlines in addition to in-app notifications.
- **Fuzzy Search Functionality:** Allows users to search for all relevant information on the site. The Fuzzy Search can handle minor typos or errors, ensuring accurate search results.
- **Download All Functionality for Secretary**: Enables the secretary to easily download all timesheets of Hiwis in bulk, streamlining the process of timesheet management.

## Technologies

- **Frontend**: The user interface is built using React, providing a dynamic and responsive experience.
- **Backend**: Python Flask serves as the backend framework, handling API requests, business logic, and data management.
- **Database (NoSQL)**: MongoDB is used for storing user data, work records, and vacation information.
- **API Communication**: REST API endpoints facilitate communication between the frontend and backend.
- **Containerization**: Docker is used to containerize the application, ensuring consistency across different development and production environments.

## Documentation

- **Pflichtenheft (Requirements Document)**: For a detailed description of project requirements and specifications, please refer to our Pflichtenheft available at [Pflichtenheft PDF](documents/Pflichtenheft/Pflichtenheft_17_05_24.pdf).
- **Entwurf (Design Document)**: For a detailed description of the project's design and architecture, please refer to our Design Document available at [Entwurf PDF](documents/Entwurfsphase/Entwurfsdokument.pdf).
- **Implementierung (Implementation Report)**: For a detailed description of the project's implementation details, please refer to our Implementation Report available at [Implementation PDF](documents/Implementierungsphase/Implementierungsbericht.pdf).
- **Quality Assurance (Quality Assurance Document)**: For a detailed description of the quality assurance process and testing procedures, please refer to our Quality Assurance Document available at [Quality Assurance PDF](documents/Quality_Assurance/Quality_Assurance.pdf).

## Installation and Setup
1. MongoDB <br>
The following command creates a MongoDB with authentication inside a Docker Container:
```
docker run --name mongoDB -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=TimeTracking123! -d mongodb/mongodb-community-server:latest
```

___

## Information around developing this project

### Git Branch strategy for this repo & dev team
1. Main branch:
   most stable version, this branch is used to deploy to production
2. Develop branch:
   contains changes that are in progress and may not be ready for production
   after all tests and the peer review have been successful, it is merged into Production
3. Features / Fixes branches:
   Branches to work on specific features and fixes. Once the feature/fix is ready, you merge it into the develop branch.

Example of a workflow with this strategy:
1. You want to develop a new feature.
2. Create a branch called "newFeatureXYZ" based on the develop branch.
3. Work on the feature in this topic branch unitil it's ready.
4. Merge "newFeatureXYZ" into the develop branch and run tests.
5. Make sure there are no merge conflicts - Change the code if necessary to resolve the conflicts - merge these changes into the develop branch
6. Everything works fine - Merge develop into main


### Installation and Setup in a Test Environment
Run the frontend
  1. Navigate to the "frontend" folder with the "cd" command in your terminal.
  2. Install all required dependencies with "npm install". Please make sure that you have Node.js installed.
  3. Start the Frontend with "npm start".

Run the backend
1. Navigate to the "backend" folder with the "cd" command in your terminal.
2. Run "pip install -r requirements.txt" to install all necessary packages.
3. Use "python -m flask run" or "flask run" to run the flask project. Please make sure that you have all required pip packages installed.
