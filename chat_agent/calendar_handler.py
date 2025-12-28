"""
Calendar Handler for Event Based Outfit System
Handles calendar-specific operations and integrations
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from event_manager import EventManager
from outfit_recommender import OutfitRecommender

class CalendarHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.event_manager = EventManager()
        self.outfit_recommender = OutfitRecommender()
        
    def process_calendar_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process calendar-related requests"""
        try:
            request_type = request_data.get('type')
            
            if request_type == 'save_event':
                return self._handle_save_event(request_data)
            elif request_type == 'get_reminders':
                return self._handle_get_reminders(request_data)
            elif request_type == 'event_outfit_suggestion':
                return self._handle_event_outfit_suggestion(request_data)
            else:
                return {
                    'success': False,
                    'message': 'Unknown calendar request type'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error processing calendar request: {e}")
            return {
                'success': False,
                'message': 'Error processing calendar request',
                'error': str(e)
            }
    
    def _handle_save_event(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle saving a new event"""
        try:
            user_email = request_data.get('user_email', 'guest@fashionpulse.com')
            event_data = {
                'gender': request_data.get('gender'),
                'date': request_data.get('date'),
                'event': request_data.get('event')
            }
            
            # Validate required fields
            if not all([event_data['gender'], event_data['date'], event_data['event']]):
                return {
                    'success': False,
                    'message': 'Missing required event information'
                }
            
            # Save event
            saved_event = self.event_manager.save_event(user_email, event_data)
            
            if saved_event:
                return {
                    'success': True,
                    'message': 'Event saved successfully!',
                    'event': saved_event
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to save event'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error saving event: {e}")
            return {
                'success': False,
                'message': 'Error saving event',
                'error': str(e)
            }
    
    def _handle_get_reminders(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting event reminders"""
        try:
            user_email = request_data.get('user_email', 'guest@fashionpulse.com')
            
            # Get upcoming events that need reminders
            reminders = self.event_manager.check_event_reminders(user_email)
            
            return {
                'success': True,
                'reminders': reminders,
                'has_reminders': len(reminders) > 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting reminders: {e}")
            return {
                'success': False,
                'message': 'Error getting reminders',
                'error': str(e)
            }
    
    def _handle_event_outfit_suggestion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting outfit suggestions for an event"""
        try:
            gender = request_data.get('gender')
            event_type = request_data.get('event_type')
            event_date = request_data.get('event_date')
            
            if not gender or not event_type:
                return {
                    'success': False,
                    'message': 'Missing gender or event type'
                }
            
            # Get outfit suggestions
            suggestions = self.outfit_recommender.get_event_outfit_suggestions(
                gender=gender,
                event_type=event_type,
                event_date=event_date
            )
            
            if suggestions['success']:
                # Format response message
                response_message = self.outfit_recommender.format_outfit_response(
                    products=suggestions['products'],
                    event_type=event_type,
                    gender=gender
                )
                
                return {
                    'success': True,
                    'response': response_message,
                    'products': suggestions['products'],
                    'categories': suggestions['categories'],
                    'event_info': suggestions['event_info']
                }
            else:
                return {
                    'success': False,
                    'message': 'Could not find outfit suggestions',
                    'error': suggestions.get('error')
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error getting event outfit suggestions: {e}")
            return {
                'success': False,
                'message': 'Error getting outfit suggestions',
                'error': str(e)
            }
    
    def check_user_has_upcoming_events(self, user_email: str) -> bool:
        """Check if user has upcoming events (for chat icon blinking)"""
        try:
            reminders = self.event_manager.check_event_reminders(user_email)
            return len(reminders) > 0
        except Exception as e:
            self.logger.error(f"❌ Error checking upcoming events: {e}")
            return False
    
    def get_event_reminder_message(self, event: Dict[str, Any]) -> str:
        """Get formatted reminder message for an event"""
        return self.event_manager.format_reminder_message(event)
    
    def validate_event_date(self, date_string: str) -> bool:
        """Validate that event date is in the future"""
        try:
            event_date = datetime.fromisoformat(date_string).date()
            today = datetime.now().date()
            return event_date >= today
        except Exception as e:
            self.logger.error(f"❌ Error validating date: {e}")
            return False
    
    def get_popular_events(self) -> List[str]:
        """Get list of popular event types for suggestions"""
        return [
            'Job Interview',
            'Wedding',
            'Birthday Party',
            'Festival',
            'Party',
            'Travel',
            'Meeting',
            'College',
            'Temple',
            'Family Function',
            'Night Out',
            'Photoshoot',
            'Date',
            'Graduation',
            'Conference',
            'Dinner',
            'Shopping',
            'Movie',
            'Concert',
            'Sports Event'
        ]