# Hacktoberfest 2023 Contributing Guidelines

![](https://hacktoberfest.com/_next/static/media/logo-hacktoberfest--horizontal.ebc5fdc8.svg)

Welcome to Hacktoberfest 2023! We're excited that you want to contribute to our project "Code Community Music". Before you get started, please take a moment to read through our contributing guidelines to ensure a smooth and productive collaboration.

## Getting Started

- Make sure you have a GitHub account. If you don't, you can sign up here.
- Fork the repository to your GitHub account.
- Clone the forked repository to your local machine.

## Code of Conduct

Please note that this project follows the Hacktoberfest Code of Conduct, and we expect all contributors to adhere to it. Be respectful, considerate, and welcoming to others.

## How to Contribute

### Reporting Issues

If you encounter any bugs, have questions, or want to propose new features, please create an issue on the GitHub repository. Make sure to provide a clear and detailed description of the problem or suggestion. We appreciate the use of templates if provided.

### Submitting Pull Request

- Check the [issue tracker](https://github.com/Abbhiishek/codecommunitymusic-server/issues) for open issues that you can work on or create a new issue if you have a -specific contribution in mind.
- Fork the repository to your GitHub account and create a new branch from the main branch. Use a descriptive branch name that reflects your contribution.
- Make your changes, following the coding guidelines mentioned below.
- Test your changes thoroughly to ensure they don't introduce new issues.
- Commit your changes with clear and concise commit messages.
- Push your branch to your GitHub fork.
- Open a pull request (PR) to the main branch of the original repository.
- Provide a detailed description of your changes in the PR description.
- Be responsive to any feedback or comments on your PR and make necessary updates.

## Getting started

- Fork this repository (Click the Fork button in the top right of this page, click your Profile Image)
- Clone your fork down to your local machine

```markdown
git clone https://github.com/Abbhiishek/codecommunitymusic-server.git
```

- Create a branch

```markdown
git checkout -b branch-name
```

- Make your changes (choose from any task below)
- Commit and push

```markdown
git add .
git commit -m 'Commit message'
git push origin branch-name
```

- Create a new pull request from your forked repository (Click the `New Pull Request` button located at the top of your repo)
- Wait for your PR review and merge approval!
- **Star this repository** if you had fun!

## Development Setup

To set up the development environment for the application, follow these steps:

- Install Python (if not already installed).



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

