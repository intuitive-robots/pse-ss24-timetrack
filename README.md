# Intuitive Time Tracking Web-App for Research Assistants

## Project Overview

This repository contains the code for a web application designed to simplify and streamline the process of time tracking for research assistants (HiWis) at Intuitive Robots Lab. The application facilitates accurate recording of work hours and ensures compliance with institutional regulations.

## Features

- **Time Entry**: Users can log their daily work hours, including start and end times, and break durations.
- **Vacation Management**: Users can request vacation days, view pending requests, and track their remaining vacation entitlement.
- **Signature Verification**: At the end of each month, users can sign their timesheets electronically, making them ready for supervisor review.
- **User Profile Management**: Users can view and update their personal information, change their password, and manage their login credentials.
- **Contract Overview**: Displays detailed contract information including assigned weekly work hours, contract start date, team details, hourly rate, and supervisor contact information.
- **Digital Signature Upload**: Users can upload a digital image of their signature for use in official documents and timesheet verification.

## Technologies

- **Frontend**: The user interface is built using React, providing a dynamic and responsive experience.
- **Backend**: Python Flask serves as the backend framework, handling API requests, business logic, and data management.
- **Database**: MongoDB is used for storing user data, work records, and vacation information.
- **API Communication**: REST API endpoints facilitate communication between the frontend and backend.
- **Containerization**: Docker is used to containerize the application, ensuring consistency across different development and production environments.

## Documentation

- **Pflichtenheft (Requirements Document)**: For a detailed description of project requirements and specifications, please refer to our Pflichtenheft available at [Pflichtenheft PDF](documents/Pflichtenheft/Pflichtenheft_17_05_24.pdf).


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
