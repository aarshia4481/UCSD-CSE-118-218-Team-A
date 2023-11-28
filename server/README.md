# Description
Goes here
# UCSD-CSE-118-218-Team-A

## Available endpoints

- `POST` /create-session
  - Request body:
    - `session_name`: string
    - `creator`: string


- `POST` /join-session
  - Request body:
    - `session_id`: string
    - `user_id`: string


- `GET` /get-sessions
    - Request body: None
    - Response body:
        - `sessions`: list of strings
