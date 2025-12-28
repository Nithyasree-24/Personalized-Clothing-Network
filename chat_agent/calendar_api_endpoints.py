"""
Calendar API Endpoints for Event Based Outfit System
Provides REST API endpoints for calendar functionality
"""
from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
from calendar_handler import CalendarHandler

# Create Blueprint for calendar endpoints
calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

# Initialize calendar handler
calendar_handler = CalendarHandler()
logger = logging.getLogger(__name__)

@calendar_bp.route('/save-event', methods=['POST'])
def save_event():
    """
    Save a new calendar event
    Expected JSON: {
        "user_email": "user@example.com",
        "gender": "Women/Men",
        "date": "2024-01-15",
        "event": "Job Interview"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Process save event request
        result = calendar_handler.process_calendar_request({
            'type': 'save_event',
            'user_email': data.get('user_email'),
            'gender': data.get('gender'),
            'date': data.get('date'),
            'event': data.get('event')
        })
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"❌ Error in save-event endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@calendar_bp.route('/get-reminders', methods=['POST'])
def get_reminders():
    """
    Get event reminders for user
    Expected JSON: {
        "user_email": "user@example.com"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_email' not in data:
            return jsonify({
                'success': False,
                'message': 'User email required'
            }), 400
        
        # Process get reminders request
        result = calendar_handler.process_calendar_request({
            'type': 'get_reminders',
            'user_email': data.get('user_email')
        })
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in get-reminders endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@calendar_bp.route('/outfit-suggestions', methods=['POST'])
def get_outfit_suggestions():
    """
    Get outfit suggestions for an event
    Expected JSON: {
        "gender": "Women/Men",
        "event_type": "Job Interview",
        "event_date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Process outfit suggestion request
        result = calendar_handler.process_calendar_request({
            'type': 'event_outfit_suggestion',
            'gender': data.get('gender'),
            'event_type': data.get('event_type'),
            'event_date': data.get('event_date')
        })
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"❌ Error in outfit-suggestions endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@calendar_bp.route('/check-upcoming', methods=['POST'])
def check_upcoming_events():
    """
    Check if user has upcoming events (for chat icon blinking)
    Expected JSON: {
        "user_email": "user@example.com"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_email' not in data:
            return jsonify({
                'success': False,
                'message': 'User email required'
            }), 400
        
        # Check for upcoming events
        has_upcoming = calendar_handler.check_user_has_upcoming_events(
            data.get('user_email')
        )
        
        return jsonify({
            'success': True,
            'has_upcoming_events': has_upcoming,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error in check-upcoming endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@calendar_bp.route('/popular-events', methods=['GET'])
def get_popular_events():
    """
    Get list of popular event types for suggestions
    """
    try:
        popular_events = calendar_handler.get_popular_events()
        
        return jsonify({
            'success': True,
            'events': popular_events,
            'count': len(popular_events)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error in popular-events endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@calendar_bp.route('/validate-date', methods=['POST'])
def validate_event_date():
    """
    Validate that event date is in the future
    Expected JSON: {
        "date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'date' not in data:
            return jsonify({
                'success': False,
                'message': 'Date required'
            }), 400
        
        # Validate date
        is_valid = calendar_handler.validate_event_date(data.get('date'))
        
        return jsonify({
            'success': True,
            'is_valid': is_valid,
            'message': 'Date is valid' if is_valid else 'Date must be in the future'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error in validate-date endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500

# Health check endpoint
@calendar_bp.route('/health', methods=['GET'])
def calendar_health_check():
    """Health check for calendar system"""
    return jsonify({
        'status': 'healthy',
        'service': 'calendar_event_system',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200