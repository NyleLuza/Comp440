Phase 1: youtube url: https://youtu.be/Ocb-vbmENkk
Phase 2: https://youtu.be/nCr4DrHcW4I?si=uWzp__uPOPLWzAUX
(audio is a bit messed up because I was recording at a cafe)

Database:
Aiven cloud (visualize on mysqlWorkbench)

Versions:
Python 3.9+
Node.js (v16+)

Installation:

# --- Install dependencies ---

pip install fastapi uvicorn pymysql
npm install

# --- Run backend ---

uvicorn server:app --reload

# --- Run frontend ---

npm start

# Step by Step Instructions for environment setup:

Step 1: Download Docker to setup environment:

- https://www.docker.com/

Step 2: cd into the client folder. This is the root folder for our frontend and run this command:

- docker run --env-file ../.env -p 3000:3000 cafestagram_client

Step 3: Ctrl + C to close the current process and go to the DockerGUI and press "Stop" so that the container is not using the same port

Step 4: run this command to run the frontend:

- npm start

Step 5: Open up a split terminal to access the server folder. This is the root folder for our backend. Run this command:

- docker run --env-file ../.env -p 8000:8000 cafestagram_server

Step 6: (repeat Step 3)

Step 7: run this command to run the backend:

- uvicorn server:app --reload
