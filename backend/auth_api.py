#!/usr/bin/env python3
"""
Authentication API Server for FashionPulse
Flask server providing authentication endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_system import AuthSystem
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize authentication system
auth_system = AuthSystem()

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({
                'success': False,
                'message': 'Name, email, and password are required.'
            }), 400
        
        # Validate email format (basic validation)
        email = data['email'].strip().lower()
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address.'
            }), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long.'
            }), 400
        
        # Attempt signup
        result = auth_system.signup(
            name=data['name'].strip(),
            email=email,
            password=data['password']
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('email', 'password')):
            return jsonify({
                'success': False,
                'message': 'Email and password are required.'
            }), 400
        
        # Attempt login
        result = auth_system.login(
            email=data['email'].strip().lower(),
            password=data['password']
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Generate password reset token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data:
            return jsonify({
                'success': False,
                'message': 'Email is required.'
            }), 400
        
        # Generate reset token
        result = auth_system.generate_reset_token(
            email=data['email'].strip().lower()
        )
        
        # In a real application, you would send this token via email
        # For now, we'll return it in the response for testing
        if result['success']:
            result['message'] = f"Password reset token: {result['token']}\n(In production, this would be sent via email)"
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('token', 'password')):
            return jsonify({
                'success': False,
                'message': 'Token and new password are required.'
            }), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long.'
            }), 400
        
        # Reset password
        result = auth_system.reset_password(
            token=data['token'],
            new_password=data['password']
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/user/chat-history', methods=['POST'])
def save_chat_history():
    """Save user's chat history"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('user_email', 'chat_data')):
            return jsonify({
                'success': False,
                'message': 'User email and chat data are required.'
            }), 400
        
        # Save chat history
        result = auth_system.save_chat_history(
            user_email=data['user_email'],
            chat_data=data['chat_data']
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/user/chat-history/<email>', methods=['GET'])
def get_chat_history(email):
    """Get user's chat history"""
    try:
        # Get chat history
        result = auth_system.get_chat_history(email)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'data': []
        }), 500

@app.route('/api/user/calendar-event', methods=['POST'])
def save_calendar_event():
    """Save user's calendar event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('user_email', 'event_data')):
            return jsonify({
                'success': False,
                'message': 'User email and event data are required.'
            }), 400
        
        # Save calendar event
        result = auth_system.save_calendar_event(
            user_email=data['user_email'],
            event_data=data['event_data']
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/user/calendar-events/<email>', methods=['GET'])
def get_calendar_events(email):
    """Get user's calendar events"""
    try:
        # Get calendar events
        result = auth_system.get_calendar_events(email)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'data': []
        }), 500

@app.route('/api/auth/test', methods=['GET'])
def test_connection():
    """Test API connection"""
    return jsonify({
        'success': True,
        'message': 'Authentication API is running!',
        'timestamp': str(datetime.now())
    })

if __name__ == '__main__':
    print("🚀 Starting FashionPulse Authentication API Server...")
    print("📍 Server will run on: http://localhost:5002")
    print("🔐 Available endpoints:")
    print("   POST /api/auth/signup")
    print("   POST /api/auth/login") 
    print("   POST /api/auth/forgot-password")
    print("   POST /api/auth/reset-password")
    print("   POST /api/user/chat-history")
    print("   GET  /api/user/chat-history/<email>")
    print("   POST /api/user/calendar-event")
    print("   GET  /api/user/calendar-events/<email>")
    print("   GET  /api/auth/test")
    
    app.run(debug=True, host='0.0.0.0', port=5002)