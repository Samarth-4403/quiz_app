import sqlite3
import hashlib

def hash_password(password):
  return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_input):
  return hashed_password == hash_password(user_input.encode('utf-8'))

def login(email, password):
  conn = sqlite3.connect('test_1.db')
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result:
      stored_hashed_password = result[0]
      if check_password(stored_hashed_password, password):
        return True  # Successful login
      else:
        return False  # Incorrect password
    else:
      return False  # User not found
  except sqlite3.Error as e:
    print(f"Error: {e}")
    return False
  finally:
    conn.close()

# Example usage (less secure!):
if login("test@example.com", "password123"):
  print("Login successful")
else:
  print("Invalid email or password")