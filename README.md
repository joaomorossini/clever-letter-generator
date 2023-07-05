# Clever Letter Generator
### AI Powered Custom Cover Letters

---

### Table of Contents
#### 1. Contact
#### 2. Features
#### 3. References
#### 4. License

---
### 1. Contact
For any queries or support, please reach out through one of the following channels:

- [GitHub](https://github.com/joaomorossini/)
- [LinkedIn](https://www.linkedin.com/in/joaomorossini/)
- [Email](mailto:ai.clever.letter@gmail.com)

---

### 2. Features
The Clever Letter Generator is a Flask-based web application that uses AI to generate custom cover letters. It includes the following features:

- User Registration and Login: Users can create an account and log in to access the cover letter generator.
- Rate Limiting: To prevent abuse, the application limits the number of requests a user can make per minute or per day.
- Secure Password Hashing: User passwords are securely hashed using Bcrypt.
- Email Support: The application uses Flask-Mail for email functionality.
- API Key Management: Users can set their own API keys for the OpenAI service.
- Cover Letter Generation: Users can generate a custom cover letter by providing details such as job title, job description, employer name, employer description, and additional instructions.
- Downloadable Cover Letters: Generated cover letters can be downloaded as text files.
- Logging: The application logs each cover letter generation event for auditing purposes.

---

### 3. References
The Clever Letter Generator uses the following libraries and services:

- Flask: A lightweight WSGI web application framework.
- Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy to your application.
- Flask-Login: Provides user session management for Flask.
- Flask-Bcrypt: Bcrypt hashing for Flask.
- Flask-Mail: A simple wrapper around smtplib.
- Flask-Limiter: Rate limiting for Flask routes.
- OpenAI: An AI model used to generate the cover letters.

---

### 4. License
This project is licensed under the terms of the MIT license. For more details, please see the LICENSE file in the project repository.