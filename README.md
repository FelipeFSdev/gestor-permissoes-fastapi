Manager system which allows you to regist users with three different "charges".
Every user has one department (example: I.T. or H.R.) and two properties which
indicates their access level, "super_user" and "is_manager".

The first one, super user, can do what he wants, with no worries about the 
department of the user. Which means the admin has access to whole system.

As manager, you only can access and/or change the record about other users in
your department. One I.T. manager only can change the name, cpf, etc; of other
users from I.T. department.

If you are not manager or super user, you are just a common user who can't do
anything (saddly) in the system.

If you want to test this project in your computer you will need to run these
commands (assuming you already have Python installed):
    • py -m venv .venv (if you want to use Poetry or other package manager, be free)
    • source .venv/Scripts/Activate (i use windows, so i don't know how it works on others O.S.)
    • pip install fastapi[standard] sqlmodel cryptocode pyjwt psycopg2
    • uvicorn main:app