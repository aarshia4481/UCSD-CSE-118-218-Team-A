# Description
Goes here
# UCSD-CSE-118-218-Team-A

## Available endpoints

- Get live metrics for a workout for yourself
https://127.0.0.1:5000/get-workout-live-metrics?alexa_id=1

- Get live metrics for a workout for a participant in the session
https://127.0.0.1:5000/get-workout-live-metrics?alexa_id=1&participant_name=Felix

- Get plan for today
https://127.0.0.1:5000/get-plan-for-today?alexa_id=1


- Get status of session
https://127.0.0.1:5000/get-status?alexa_id=1
Not really necessary rn. The user joins or creates a session on the watch. Then we could start a session from there instead of via Alexa.



###Endpoints from the old API for original idea

- `POST` /create-session 
- Creates a new session and returns the created session.
  - Request body:
    - `session_name`: string
    - `creator_id`: string


- `POST` /join-session
- Adds a user to a existing session and returns the session.
- Request body:
  - `session_name`: string
  - `user_id`: string


- `GET` /get-sessions
- Returns a list of all sessions.
    - Request body: None
    - Response body:
        - `sessions`: list of strings
