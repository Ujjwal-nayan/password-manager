import os
import sqlite3
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "vault.db")
KEY_FILE = os.path.join(BASE_DIR, "secret.key")

db_exists = os.path.exists(DB_FILE)
key_exists = os.path.exists(KEY_FILE)

# First run: create a new key
if not key_exists:
    if db_exists:
        print("❌ Error: secret.key is missing.")
        print("Your passwords cannot be decrypted without the original key.")
        exit()

    with open(KEY_FILE, "wb") as file:
        file.write(Fernet.generate_key())

with open(KEY_FILE, "rb") as file:
    key = file.read()

cipher = Fernet(key)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS master(
    id INTEGER PRIMARY KEY,
    password_hash TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    encrypted_password TEXT NOT NULL
)
""")

conn.commit()

# print("Database initialized!")

cursor.execute("SELECT * FROM master")

master = cursor.fetchone()

if master is None:
    password = getpass("Create master password: ")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "INSERT INTO master(password_hash) VALUES(?)",
        (password_hash,)
    )

    conn.commit()

    print("✅ Master password created.")

else:
    password = getpass("Enter master password: ")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash != master[1]:
        print("❌ Wrong password.")
        conn.close()
        exit()

    print("✅ Access granted.\n")

def add_password():
    while True:
        website = input("Website: ").strip()

        if website != "":
            break

        print("Website cannot be empty.")

    while True:
        username = input("Username: ").strip()

        if username != "":
            break

        print("Username cannot be empty.")

    while True:
        password = input("Password: ").strip()

        if password != "":
            break

        print("Password cannot be empty.")

    encrypted_password = cipher.encrypt(password.encode()).decode()

    cursor.execute(
        """
        INSERT INTO passwords(website, username, encrypted_password)
        VALUES(?, ?, ?)
        """,
        (website, username, encrypted_password)
    )

    conn.commit()

    print("✅ Password saved.")

def view_passwords():
    cursor.execute("SELECT * FROM passwords")

    passwords = cursor.fetchall()

    if not passwords:
        print("No passwords saved.")
        return

    print()

    for password in passwords:
        decrypted_password = cipher.decrypt(
            password[3].encode()
        ).decode()

        print(f"ID       : {password[0]}")
        print(f"Website  : {password[1]}")
        print(f"Username : {password[2]}")
        print(f"Password : {decrypted_password}")
        print("-" * 30)

def search_password():
    while True:
        website = input("Website: ").strip()

        if website != "":
            break

        print("Website cannot be empty.")

    cursor.execute(
        "SELECT * FROM passwords WHERE website = ?",
        (website,)
    )

    password = cursor.fetchone()

    if password is None:
        print("Password not found.")
        return

    decrypted_password = cipher.decrypt(
        password[3].encode()
    ).decode()

    print(f"\nWebsite  : {password[1]}")
    print(f"Username : {password[2]}")
    print(f"Password : {decrypted_password}")

def delete_password():
    while True:
        website = input("Website to delete: ").strip()

        if website != "":
            break

        print("Website cannot be empty.")

    cursor.execute(
        "SELECT * FROM passwords WHERE website = ?",
        (website,)
    )

    password = cursor.fetchone()

    if password is None:
        print("Password not found.")
        return

    confirm = input(f"Delete password for {website}? (y/n): ").strip().lower()

    if confirm == "y":
        cursor.execute(
            "DELETE FROM passwords WHERE website = ?",
            (website,)
        )

        conn.commit()

        print("✅ Password deleted.")
    else:
        print("Cancelled.")

while True:
    print("""
===== PASSWORD MANAGER =====
1. Add Password
2. View Passwords
3. Search Password
4. Delete Password
5. Exit
============================
""")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        add_password()

    elif choice == "2":
        view_passwords()

    elif choice == "3":
        search_password()

    elif choice == "4":
        delete_password()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")

conn.close()
