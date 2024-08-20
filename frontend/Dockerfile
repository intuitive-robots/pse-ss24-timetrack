# Step 1: Build the React app
FROM node:16 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}

# Build the React app for production
RUN npm run build
RUN npm install -g serve

# Expose port 80 to the outside world
EXPOSE 80

# Start nginx when the container starts
CMD ["serve", "-s", "build", "-l", "80"]