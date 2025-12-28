#!/usr/bin/env python3
"""
User Authentication System for FashionPulse
Handles signup, login, password reset, and user session management
Connected to existing fashiopulse database
"""

import mysql.connector
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os

class AuthSystem:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Update with your MySQL password if needed
            'database': 'fashiopulse'
        }
        self.init_database()
    
    def init_database(self):
        """Initialize the users table if it doesn't exist"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if users table exists, if not create it
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                # Create users table
                cursor.execute("""
                    CREATE TABLE users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reset_token VARCHAR(255) NULL,
                        reset_token_expires TIMESTAMP NULL
                    )
                """)
                print("✅ Users table created successfully")
            else:
                # Check if reset token columns exist, add them if not
                cursor.execute("SHOW COLUMNS FROM users LIKE 'reset_token'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255) NULL")
                    cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP NULL")
                    print("✅ Added reset token columns to existing users table")
            
            # Create user_chat_history table if it doesn't exist
            cursor.execute("SHOW TABLES LIKE 'user_chat_history'")
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE user_chat_history (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_email VARCHAR(255) NOT NULL,
                        chat_data JSON NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_user_email (user_email)
                    )
                """)
                print("✅ User chat history table created successfully")
            
            # Create user_calendar_events table if it doesn't exist
            cursor.execute("SHOW TABLES LIKE 'user_calendar_events'")
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE user_calendar_events (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_email VARCHAR(255) NOT NULL,
                        event_data JSON NOT NULL,
                        event_date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_user_email (user_email),
                        INDEX idx_event_date (event_date)
                    )
                """)
                print("✅ User calendar events table created successfully")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database connection successful - fashiopulse database ready")
            
        except mysql.connector.Error as e:
            print(f"❌ Database initialization error: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self, name, email, password):
        """
        Register a new user
        Returns: {'success': bool, 'message': str}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'You already have an account. Please login instead.'
                }
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Account created successfully! Please login with your credentials.'
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def login(self, email, password):
        """
        Authenticate user login
        Returns: {'success': bool, 'message': str, 'user': dict}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'No account found with this email. Please sign up first.',
                    'show_signup': True
                }
            
            # Verify password
            hashed_password = self.hash_password(password)
            if user[3] != hashed_password:
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'Incorrect password. Please try again.',
                    'show_forgot': True
                }
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Login successful! Welcome back.',
                'user': {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database connection error: {str(e)}'
            }
    
    def generate_reset_token(self, email):
        """
        Generate password reset token
        Returns: {'success': bool, 'message': str, 'token': str}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'No account found with this email. Please sign up first.'
                }
            
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            
            # Update user with reset token
            cursor.execute(
                "UPDATE users SET reset_token = %s, reset_token_expires = %s WHERE email = %s",
                (reset_token, expires_at, email)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Password reset link sent! Use this token to reset your password.',
                'token': reset_token
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def reset_password(self, token, new_password):
        """
        Reset password using token
        Returns: {'success': bool, 'message': str}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if token is valid and not expired
            cursor.execute(
                "SELECT email FROM users WHERE reset_token = %s AND reset_token_expires > %s",
                (token, datetime.now())
            )
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'Invalid or expired reset token. Please request a new one.'
                }
            
            # Update password and clear reset token
            hashed_password = self.hash_password(new_password)
            cursor.execute(
                "UPDATE users SET password = %s, reset_token = NULL, reset_token_expires = NULL WHERE reset_token = %s",
                (hashed_password, token)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Password reset successful! You can now login with your new password.'
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def save_chat_history(self, user_email, chat_data):
        """
        Save user's chat history
        Returns: {'success': bool, 'message': str}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Insert chat history
            cursor.execute(
                "INSERT INTO user_chat_history (user_email, chat_data) VALUES (%s, %s)",
                (user_email, json.dumps(chat_data))
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Chat history saved successfully.'
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_chat_history(self, user_email):
        """
        Get user's chat history
        Returns: {'success': bool, 'data': list}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT chat_data, created_at FROM user_chat_history WHERE user_email = %s ORDER BY created_at DESC LIMIT 10",
                (user_email,)
            )
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'chat_data': json.loads(row[0]),
                    'created_at': row[1].isoformat()
                })
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'data': history
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}',
                'data': []
            }
    
    def save_calendar_event(self, user_email, event_data):
        """
        Save user's calendar event
        Returns: {'success': bool, 'message': str}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Extract event date
            event_date = datetime.strptime(event_data['date'], '%Y-%m-%d').date()
            
            # Insert calendar event
            cursor.execute(
                "INSERT INTO user_calendar_events (user_email, event_data, event_date) VALUES (%s, %s, %s)",
                (user_email, json.dumps(event_data), event_date)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Calendar event saved successfully.'
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}'
            }
    
    def get_calendar_events(self, user_email):
        """
        Get user's calendar events
        Returns: {'success': bool, 'data': list}
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT event_data, event_date, created_at FROM user_calendar_events WHERE user_email = %s ORDER BY event_date ASC",
                (user_email,)
            )
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'event_data': json.loads(row[0]),
                    'event_date': row[1].isoformat(),
                    'created_at': row[2].isoformat()
                })
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'data': events
            }
            
        except mysql.connector.Error as e:
            return {
                'success': False,
                'message': f'Database error: {str(e)}',
                'data': []
            }

# Test the system
if __name__ == "__main__":
    auth = AuthSystem()
    
    print("🔍 Testing FashionPulse Authentication System...")
    print("📍 Connected to: fashiopulse database")
    print("📊 Table: users")
    
    # Test signup
    print("\n1️⃣ Testing signup...")
    result = auth.signup("Test User", "test@fashionpulse.com", "password123")
    print(f"Signup result: {result}")
    
    # Test login
    print("\n2️⃣ Testing login...")
    result = auth.login("test@fashionpulse.com", "password123")
    print(f"Login result: {result}")
    
    # Test wrong password
    print("\n3️⃣ Testing wrong password...")
    result = auth.login("test@fashionpulse.com", "wrongpassword")
    print(f"Wrong password result: {result}")
    
    # Test non-existent email
    print("\n4️⃣ Testing non-existent email...")
    result = auth.login("nonexistent@fashionpulse.com", "password123")
    print(f"Non-existent email result: {result}")
    
    # Test duplicate signup
    print("\n5️⃣ Testing duplicate signup...")
    result = auth.signup("Another User", "test@fashionpulse.com", "newpassword")
    print(f"Duplicate signup result: {result}")
    
    print("\n✅ All tests completed!")