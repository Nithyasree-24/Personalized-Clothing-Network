"""
Event Manager for Calendar Event Based Outfit Personalization System
Handles event storage, retrieval, and reminder logic
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class EventManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def save_event(self, user_email: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user event to localStorage-like storage"""
        try:
            # Create event with unique ID
            event = {
                'id': f"event_{datetime.now().timestamp()}_{hash(user_email)}",
                'user_email': user_email,
                'gender': event_data.get('gender'),
                'date': event_data.get('date'),
                'event': event_data.get('event'),
                'created_at': datetime.now().isoformat(),
                'status': 'active'  # active, completed, cancelled
            }
            
            self.logger.info(f"📅 Event saved for {user_email}: {event['event']} on {event['date']}")
            return event
            
        except Exception as e:
            self.logger.error(f"❌ Error saving event: {e}")
            return {}
    
    def get_upcoming_events(self, user_email: str, days_ahead: int = 3) -> List[Dict[str, Any]]:
        """Get upcoming events for user within specified days"""
        try:
            # In a real implementation, this would query a database
            # For now, we'll simulate the logic
            today = datetime.now().date()
            future_date = today + timedelta(days=days_ahead)
            
            # This would be replaced with actual database query
            # For demo purposes, we'll return empty list
            # The frontend handles the actual storage via localStorage
            
            self.logger.info(f"🔍 Checking upcoming events for {user_email}")
            return []
            
        except Exception as e:
            self.logger.error(f"❌ Error getting upcoming events: {e}")
            return []
    
    def check_event_reminders(self, user_email: str) -> List[Dict[str, Any]]:
        """Check if user has events that need reminders"""
        try:
            upcoming_events = self.get_upcoming_events(user_email, days_ahead=3)
            
            reminders = []
            for event in upcoming_events:
                event_date = datetime.fromisoformat(event['date']).date()
                today = datetime.now().date()
                days_until = (event_date - today).days
                
                if days_until <= 3:  # Remind 3 days before
                    reminders.append({
                        **event,
                        'days_until': days_until,
                        'reminder_type': 'upcoming'
                    })
            
            return reminders
            
        except Exception as e:
            self.logger.error(f"❌ Error checking event reminders: {e}")
            return []
    
    def get_event_categories(self, gender: str, event_type: str) -> List[str]:
        """Get recommended categories based on gender and event type"""
        
        event_type_lower = event_type.lower()
        
        if gender.lower() == 'women':
            # Women's event-based recommendations
            if any(keyword in event_type_lower for keyword in ['job', 'interview', 'office', 'meeting', 'work']):
                return ['Western Wear', 'Tops and Co-ord Sets', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['wedding', 'engagement', 'reception', 'marriage']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['birthday', 'party', 'night out', 'celebration', 'club']):
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
            elif any(keyword in event_type_lower for keyword in ['college', 'daily', 'casual', 'university', 'school']):
                return ['Tops and Co-ord Sets', 'Western Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['festival', 'diwali', 'pongal', 'navratri', 'eid', 'onam', 'traditional']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['family', 'temple', 'religious', 'function']):
                return ['Ethnic Wear', 'Dresses']
            elif any(keyword in event_type_lower for keyword in ['travel', 'trip', 'photoshoot', 'vacation', 'holiday']):
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
            else:
                # Default for women
                return ['Western Wear', 'Dresses', 'Tops and Co-ord Sets']
        
        else:  # men
            # Men's event-based recommendations
            if any(keyword in event_type_lower for keyword in ['job', 'interview', 'office', 'meeting', 'work']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['wedding', 'engagement', 'reception', 'marriage']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['party', 'celebration', 'night out', 'club']):
                return ['Shirts', 'T-shirts']
            elif any(keyword in event_type_lower for keyword in ['college', 'daily', 'casual', 'university', 'school']):
                return ['T-shirts', 'Shirts']
            elif any(keyword in event_type_lower for keyword in ['festival', 'diwali', 'pongal', 'eid', 'onam', 'traditional']):
                return ['Shirts']
            elif any(keyword in event_type_lower for keyword in ['travel', 'trip', 'photoshoot', 'vacation', 'holiday']):
                return ['Shirts', 'T-shirts']
            else:
                # Default for men
                return ['Shirts', 'T-shirts']
    
    def format_reminder_message(self, event: Dict[str, Any]) -> str:
        """Format reminder message for event"""
        try:
            event_date = datetime.fromisoformat(event['date']).strftime('%B %d, %Y')
            days_until = event.get('days_until', 0)
            
            if days_until == 0:
                time_text = "today"
            elif days_until == 1:
                time_text = "tomorrow"
            else:
                time_text = f"in {days_until} days"
            
            message = f"🔔 **Event Reminder**\n\n"
            message += f"Your event \"{event['event']}\" on {event_date} is {time_text}!\n\n"
            message += f"Here are the best outfit suggestions for you:"
            
            return message
            
        except Exception as e:
            self.logger.error(f"❌ Error formatting reminder message: {e}")
            return "🔔 You have an upcoming event!"