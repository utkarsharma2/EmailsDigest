# EmailsDigest
## Introduction
   A webserver to convert bulk emails to more managable form. **[More Info](https://utkarsharma2.medium.com/adding-meaning-back-to-alert-emails-db6b44aa24b4)**
## Setup
    - Prerequisite
      - Pyhton3
      - pip
      - [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
      - [celery](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html)
    - navigate to root of the folder where you cloned this repo
    - setup environment
      - command: virtualenv env
      - command: source env/bin/activate
    - install dependencies
      - command: pip install -r requirements.txt
    - congigure email: nativate to <project root>/Server/Server/settings.py
        - Replace 'yourEmail@gmail.com' and 'yourPassword' with your email and gmail generated password respectively.
    - start django server
      - command: python3 Server/manage.py migrate
      - command: python3 Server/manage.py runserver
    - start celery
      - command: celery -A Server worker -l INFO

## To Run:
    - Create a Application via django admin
      - visit http://localhost:8000/admin/
    - Now we need to enqueue emails
      - hit API with [postman](https://www.postman.com/) or similar client with required params or use curl request
        ```
        curl --location --request POST 'localhost:8000/emailsdigest/api/v1/enqueue/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
          "subject" : "xyz",
          "body": "xyz",
          "app": "dummy"
        }'
        ```
      - Enqueue multiple emails to see how they are grouped and combined in a digest.
    - Now that we have emails enqueue we ask server to send emails
      - command: python3 Server/manage.py send_emails

## Tech Stack
- Python3
- Django 3.1