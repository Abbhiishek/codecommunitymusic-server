## Code for Community Backend Service Readme


Welcome to the Code for Community Backend Service! This Django application serves as the backend for the Code for Community page, providing essential functionality and APIs. This README will guide you through the setup process, including creating a virtual environment, running necessary commands, and configuring an SMTP server for sending emails.



### Prerequisites
Before you begin, ensure you have the following installed on your system:

- Python 3.x
- pip (Python package manager)


### Setup Instructions


1. Clone the repository to your local machine.

```bash
git clone https://github.com/Abbhiishek/codecommunitymusic-server.git
```

2. Change into the project directory:
    
    ```bash
    cd codecommunitymusic-server
    ```
3. Create a virtual environment and activate it using python's venv module

    ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

4. Activate the virtual environment:

    - On macos
    ```bash
    source venv/bin/activate
    ```
    - On Windows
    ```bash
    venv\Scripts\activate
    ```


5. Install the required packages using pip

    ```bash
    pip install -r requirements.txt
    ```

6. Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

7. Create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:

    ```bash
    python manage.py runserver
    ```

9. Open the development server in your browser at "http://localhost:8000/"


### SMTP Configuration

This application uses SMTP to send emails, such as account verification and password reset emails. To configure SMTP, follow these steps:

1. Create a file named ".env" in the project root directory.

2. Add the following lines to the file, replacing the values with your own:

    ```bash
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = <your email address>
    EMAIL_HOST_PASSWORD = <your email password>
    ```


    >> Note: For security reasons, it's recommended to use environment variables to store sensitive information like email passwords.


3. Save the file and restart the development server.

