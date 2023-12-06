# Description
Goes here
# UCSD-CSE-118-218-Team-A

## Available endpoints

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
