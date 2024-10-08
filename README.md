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
- **Activity Type**: Each time entry includes a field to specify the type of activity, with two available options: "Project Work" or "Project Meeting."
- **Digital Signature Upload**: Users can upload a digital image of their signature for use in official documents and timesheet verification.
- **Comprehensive Time Entry Validation**: Time Entries undergo extensive validation using multiple strategies. This includes format input validation, checks for weekends or holidays, ensuring that regular working hours are not exceeded by more than 2 hours, and verifying that break times are adhered to.
- **Notification Integration** In-app notifications inform users of important updates, such as status changes and deadlines.
- **Slack Integration:** Integrates with the Slack API to provide additional notifications to users via Slack, reminding them of status changes or upcoming deadlines in addition to in-app notifications.
- **Fuzzy Search Functionality:** Allows users to search for all relevant information on the site. The Fuzzy Search can handle minor typos or errors, ensuring accurate search results.
- **Download All Functionality for Secretary**: Enables the secretary to easily download all timesheets of Hiwis in bulk, streamlining the process of timesheet management.
- **User Archiving**: Administrators can archive users, effectively hiding all user-specific information. Archived users can be reactivated at any time, restoring their information when needed.
- **Dynamic Profile Picture**: Profile pictures are automatically generated using a hash of the user's first and last name, providing a consistent background color for each user. This approach saves storage space by eliminating the need to store individual profile images.

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
Important note:
To deploy the web app using Docker, make sure to use the [Docker-Deployment branch](https://github.com/intuitive-robots/pse-ss24-timetrack/tree/Docker-Deployment). All other branches are intended for testing and are not suitable for production use.

 
### 1. MongoDB <br>
The following command creates a MongoDB with authentication inside a Docker Container:
```
docker run --name mongoDB -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=<choose-db-username> -e MONGO_INITDB_ROOT_PASSWORD=<choose-db-password> -d mongodb/mongodb-community-server:latest
```
### 2. Flask-Backend <br>
#### 2.1 Generate the image
   - Generate the backend image with the following command:
   ```
   docker build --build-arg REACT_APP_BACKEND_URL=http://<your-backend-ip>:<your-backend-port> -t clockwise_backend .
   ```
#### 2.2 Run the image within a container
   - Use the following command to run a Docker container with the image
   ```
   docker run --name clockwise_backend -e DB_HOST=<your-db-ip> -e DB_USERNAME=<your-db-username> -e DB_PASSWORD=<your-db-password> -d -p 5001:5001 clockwise_backend:latest
   ```
   - When the backend is started for the first time, the system generates a default admin account (username: irladmin, password: irl123). This admin can then create additional users, such as assistants (Hiwis), supervisors, and others. We strongly recommend changing the password as soon as possible.
### 3. React-Frontend

#### 3.1 Find out IP-Address
   - Determine the IP address of the system that is running the Docker instance.

####   3.2 Modify `nginx.conf` file within the `/frontend` directory
   - Replace every `proxy_pass` IP with your own Backend IP Address.
   - Don't change the port `5001`.

#### 3.3 Modify `package.json` file within the `/frontend`directory
   - Replace the `proxy`IP with your own Backend IP Address (incl. the port 5001).

####   3.4 Generate the image
   - Generate the Docker image with the following command:
     ```
     docker build --build-arg REACT_APP_BACKEND_URL=http://<your-backend-ip>:5001 -t clockwise_frontend .
     ```

####   3.5 Run the image within a container
   - Use the following command to run the image inside a container:
     ```
     docker run --name clockwise_frontend -d -p 80:80 clockwise_frontend:latest
     ```
### 4. Slack Integration
The Slack integration is used to send notifications, such as when the status of a timesheet changes or when a user needs to be reminded to sign a timesheet.

#### 4.1 Retrieve Slack API Token
   - Follow the `Create an App` Section within the quickstart guide [Slack-App Quickstart Guide](https://api.slack.com/quickstart)
   - Inside the `Display Information` enter Clockwise as the App name
   - Inside the `OAuth & Permissions` section, add the chat:write scope to allow the integration to send messages.
   - To retrieve the OAuth token you have to install the app to your workspace
   - After that you should be able to see a `Bot User OAuth Token` within the OAuth Tokens section.

#### 4.2 Write the token into the DB
   - Log in to your MongoDB database and open the `administration` collection. By default, there is already an entry with an empty value in the `slackToken` field. You need to insert the OAuth token here.
   - Finished! The application will detect the token automatically.
___

## Information around developing this project

### Git Branch strategy for this repo & dev team
1. Main branch:
   most stable version
2. Docker-Deployment branch:
   used to create docker images and to deploy the Web-App
3. Develop branch:
   contains changes that are in progress and may not be ready for production
   after all tests and the peer review have been successful, it is merged into Production
4. Features / Fixes branches:
   Branches to work on specific features and fixes. Once the feature/fix is ready, you merge it into the develop branch.

#### Example of a workflow with this strategy:
1. You want to develop a new feature.
2. Create a branch called "newFeatureXYZ" based on the develop branch.
3. Work on the feature in this topic branch unitil it's ready.
4. Merge "newFeatureXYZ" into the develop branch and run tests.
5. Make sure there are no merge conflicts - Change the code if necessary to resolve the conflicts - merge these changes into the develop branch
6. Everything works fine - Merge develop into main
7. Want to create a docker image? Merge into Docker-Deployment and follow the documentation above.


### Installation and Setup in a Test Environment
#### Run the frontend
1. Navigate to the "frontend" folder with the "cd" command in your terminal.
2. Install all required dependencies with "npm install". Please make sure that you have Node.js installed.
3. Start the Frontend with "npm start".

#### Run the backend
1. Navigate to the "backend" folder with the "cd" command in your terminal.
2. Run "pip install -r requirements.txt" to install all necessary packages.
3. Use "python -m flask run" or "flask run" to run the flask project. Please make sure that you have all required pip packages installed.

