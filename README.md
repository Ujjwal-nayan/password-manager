# CLI Password Manager

A secure command-line password manager built with Python, SQLite, and Fernet encryption.

This project stores account credentials in an SQLite database while encrypting passwords before they are saved. A master password is required to access the vault, and only its SHA-256 hash is stored in the database.

## Features

* Create and verify a master password
* Store encrypted passwords securely
* View saved credentials
* Search passwords by website
* Delete saved passwords
* Automatic database creation on first run
* Automatic encryption key generation
* Input validation for user entries

## Tech Stack

* Python
* SQLite
* Cryptography (Fernet)

## Project Structure

```text
password-manager/
├── password_manager.py
├── requirements.txt
├── .gitignore
├── README.md
├── vault.db        # Generated automatically
└── secret.key      # Generated automatically
```

> `vault.db` and `secret.key` are excluded from Git using `.gitignore`.

## Installation

Clone the repository:

```bash
git clone https://github.com/Ujjwal-nayan/password-manager.git
```

Move into the project directory:

```bash
cd password-manager
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python password_manager.py
```

On the first run, the application automatically creates:

* `vault.db`
* `secret.key`

and prompts you to create a master password.

## Security Notes

* The master password is stored as a SHA-256 hash.
* Account passwords are encrypted using Fernet before being saved.
* Password input is hidden using `getpass`.
* The encryption key and database are ignored by Git and remain local.

## What I Learned

This project helped me understand:

* SQLite database operations
* Parameterized SQL queries
* Password hashing
* Symmetric encryption with Fernet
* Authentication flow
* Input validation
* Organizing a larger Python project

## Future Improvements

* Edit existing passwords
* Generate strong passwords
* Password strength checker
* Export and import vault
* GUI or web interface

## Author

**Ujjwal Nayan**

GitHub: https://github.com/Ujjwal-nayan
