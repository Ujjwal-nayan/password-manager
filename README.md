# CLI Password Manager

A secure command-line password manager built with Python, SQLite, and Fernet encryption.

Passwords are encrypted before being stored in an SQLite database. A master password is required to access the vault — only its bcrypt hash is stored, never the password itself.

## Features

- Create and verify a master password (hashed with bcrypt)
- Store encrypted passwords securely using Fernet
- View all saved credentials
- Search passwords by website (case-insensitive)
- Delete passwords by ID (safe when multiple accounts exist for the same website)
- Hidden input for both master and stored passwords via `getpass`
- Automatic database and encryption key generation on first run
- Input validation throughout

## Tech Stack

- Python
- SQLite
- cryptography (Fernet)
- bcrypt

## Project Structure

```text
password-manager/
├── password_manager.py
├── requirements.txt
├── .gitignore
└── README.md
```

> `vault.db` and `secret.key` are generated on first run and excluded from Git via `.gitignore`.

## Installation

```bash
git clone https://github.com/Ujjwal-nayan/password-manager.git
cd password-manager
pip install -r requirements.txt
python password_manager.py
```

On first run, the app automatically creates `vault.db` and `secret.key`, then prompts you to set a master password.

## Security Notes

- Master password is hashed with **bcrypt** (slow by design, resistant to brute force)
- Stored passwords are encrypted with **Fernet** symmetric encryption before saving
- All password input is hidden using `getpass` — nothing is visible on screen while typing
- `vault.db` and `secret.key` never leave your machine (excluded from Git)
- **Important:** Keep `secret.key` backed up separately. If it is lost, your stored passwords cannot be recovered.

## What I Learned

- SQLite database operations and parameterized queries
- Password hashing with bcrypt vs plain SHA-256 (and why it matters)
- Symmetric encryption with Fernet
- Authentication flow for a local vault
- Safe deletion by primary key to avoid bulk deletes
- Secure input handling with `getpass`

## Future Improvements

- Edit existing passwords
- Random strong password generator
- Password strength checker
- Export / import vault
- GUI or web interface

## Author

**Ujjwal Nayan**  
GitHub: https://github.com/Ujjwal-nayan
