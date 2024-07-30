# Test-task-StarNavi

# Description

This project is an API for managing contacts, users, and comments implemented with FastAPI. The API provides basic CRUD (create, read, update, delete) operations for contacts, as well as authentication, authorization, and comment management.

# Main functionalities

1. Authentication and authorization
- Signup (POST /api/auth/signup): Registration of a new user. You need to provide username, email and password. Response: new user data.
- Login (POST /api/auth/login): Log in to the system. You must provide username (email) and password. Response: access and update tokens.
- Refresh Token (GET /api/auth/refresh_token): Refresh access and upgrade tokens. Requires the Authorization header with the refresh token. Response: new tokens.
2. Contacts
- Get Contacts (GET /api/contacts/): Get the list of contacts. Request parameters: limit and offset.
- Get Contact by ID (GET /api/contacts/{contact_id}): Get contacts by their ID.
- Create Contact (POST /api/contacts/): Create a new contact. You need to provide contact details.
- Update Contact (PUT /api/contacts/{contact_id}): Updates an existing contact by its ID.
- Delete Contact (DELETE /api/contacts/{contact_id}): Delete a contact by its ID.
- Set Favorite (PATCH /api/contacts/{contact_id}/favorite): Change the status of a favorite contact.
3. Search for contacts
- Search by First Name (GET /api/search/firstname/{firstname}): Search for contacts by first name.
- Search by Last Name (GET /api/search/lastname/{lastname}): Search for contacts by last name.
- Search by Email (GET /api/search/email/{email}): Search for contacts by email.
- Search by Phone (GET /api/search/phone/{phone}): Search for contacts by phone.
- Get Birthday List (GET /api/search/shift/{shift}): Get a list of contacts whose birthday is in shift days.
4. Comments.
- Create Comment (POST /api/comments/): Add a new comment to a post. You need to provide content and post_id.
- Read Comments (GET /api/comments/): Get the list of comments with skip and limit parameters.
- Read Comment by ID (GET /api/comments/{comment_id}): Get a comment by its ID.
- Update Comment (PUT /api/comments/{comment_id}): Update a comment by its ID.
- Delete Comment (DELETE /api/comments/{comment_id}): Deletes a comment by its ID.
- Block Comment (POST /api/comments/block/{comment_id}): Block a comment.
- Comments Daily Breakdown (GET /api/comments-daily-breakdown): Get a daily breakdown of comments for a specific period (date_from and date_to).



# Installation
1. Use venv to create a virtual environment:

    1.1. to create a new virtual environment, run the command in the console:

        - python -m venv venv

    1.2. to activate the new virtual environment, run the command in the console:

        - venv\Scripts\activate.bat (Windows)
        - source venv/bin/activate (Linux / Mac OS)

     1.3. to deactivate the new virtual environment, run the command in the console:

        - deactivate

2. To install all dependencies after activating the new virtual environment, run the following command in the console:

        - pip install -r requirements.txt
3.  Run the following command to start the FastAPI server with uvicorn:

        - uvicorn main:app --host localhost --port 8000 --reload

OpenAPI documentation : http://127.0.0.1:8000/docs

# Screenshots of the program


![Screenshot](https://github.com/SoniaDudiy/Test-task-StarNavi/blob/main/fastapi%201.png)

![Screenshot](https://github.com/SoniaDudiy/Test-task-StarNavi/blob/main/fastapi%202.png)

![Screenshot](https://github.com/SoniaDudiy/Test-task-StarNavi/blob/main/fastapi%203.png)


# API tests can be run using 

- testing of comments - pytest tests/test_unit_repository_comments.py
- testing of contacts - pytest tests/test_unit_repository_contacts.py
- testing of users - pytest tests/test_unit_repository_users.py
- search testing - pytest tests/test_unit_repository_search.py

            
