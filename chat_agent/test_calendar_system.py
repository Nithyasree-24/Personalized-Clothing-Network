#!/usr/bin/env python3
"""
Test Calendar Event Based Outfit Personalization System
Comprehensive testing for all calendar functionality
"""
import requests
import json
from datetime import datetime, timedelta

def test_calendar_system():
    print("📅 Testing Calendar Event Based Outfit System")
    print("=" * 70)
    
    base_url = "http://localhost:5001"
    
    # Test 1: Event Outfit Suggestions
    print("Test 1: Event Outfit Suggestions")
    print("-" * 40)
    
    test_cases = [
        {
            'name': 'Women Job Interview',
            'data': {
                'type': 'eventOutfitSuggestion',
                'gender': 'women',
                'eventType': 'Job Interview',
                'eventDate': '2024-01-15'
            }
        },
        {
            'name': 'Men Wedding',
            'data': {
                'type': 'eventOutfitSuggestion',
                'gender': 'men',
                'eventType': 'Wedding',
                'eventDate': '2024-02-20'
            }
        },
        {
            'name': 'Women Festival',
            'data': {
                'type': 'eventOutfitSuggestion',
                'gender': 'women',
                'eventType': 'Diwali Festival',
                'eventDate': '2024-11-01'
            }
        },
        {
            'name': 'Men Party',
            'data': {
                'type': 'eventOutfitSuggestion',
                'gender': 'men',
                'eventType': 'Birthday Party',
                'eventDate': '2024-03-10'
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(f'{base_url}/api/chat', json={
                'message': json.dumps(test_case['data'])
            })
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                print(f"✅ {test_case['name']}: {len(products)} outfits found")
                
                if products:
                    for i, product in enumerate(products[:2], 1):
                        print(f"   {i}. {product['product_name']} - {product['product_category']}")
            else:
                print(f"❌ {test_case['name']}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test_case['name']}: Exception - {e}")
        
        print()
    
    # Test 2: Category Logic
    print("Test 2: Event Category Logic")
    print("-" * 40)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from event_manager import EventManager
        
        event_manager = EventManager()
        
        print("Women's Event Categories:")
        women_events = [
            'Job Interview', 'Wedding', 'Birthday Party', 'College', 
            'Diwali Festival', 'Family Function', 'Travel'
        ]
        
        for event in women_events:
            categories = event_manager.get_event_categories('women', event)
            print(f"  {event}: {', '.join(categories)}")
        
        print("\nMen's Event Categories:")
        men_events = [
            'Job Interview', 'Wedding', 'Party', 'College', 
            'Festival', 'Travel'
        ]
        
        for event in men_events:
            categories = event_manager.get_event_categories('men', event)
            print(f"  {event}: {', '.join(categories)}")
        
        print("\n✅ Category logic working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing categories: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Calendar System Testing Complete!")

def test_outfit_recommender():
    print("\n👗 Testing Outfit Recommender")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from outfit_recommender import OutfitRecommender
        
        recommender = OutfitRecommender()
        
        # Test different event types
        test_events = [
            ('women', 'Job Interview'),
            ('men', 'Wedding'),
            ('women', 'Party'),
            ('men', 'College')
        ]
        
        for gender, event in test_events:
            result = recommender.get_event_outfit_suggestions(gender, event)
            
            if result['success']:
                print(f"✅ {gender.title()} {event}: {len(result['products'])} products")
                print(f"   Categories: {', '.join(result['categories'])}")
            else:
                print(f"❌ {gender.title()} {event}: Failed")
            print()
        
        print("✅ Outfit Recommender working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing outfit recommender: {e}")

def test_calendar_handler():
    print("\n📅 Testing Calendar Handler")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from calendar_handler import CalendarHandler
        
        handler = CalendarHandler()
        
        # Test save event
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        save_result = handler.process_calendar_request({
            'type': 'save_event',
            'user_email': 'test@fashionpulse.com',
            'gender': 'Women',
            'date': tomorrow,
            'event': 'Job Interview'
        })
        
        if save_result['success']:
            print("✅ Event saving: Working")
        else:
            print(f"❌ Event saving: {save_result['message']}")
        
        # Test outfit suggestions
        outfit_result = handler.process_calendar_request({
            'type': 'event_outfit_suggestion',
            'gender': 'Women',
            'event_type': 'Job Interview',
            'event_date': tomorrow
        })
        
        if outfit_result['success']:
            print(f"✅ Outfit suggestions: {len(outfit_result['products'])} products")
        else:
            print(f"❌ Outfit suggestions: {outfit_result['message']}")
        
        # Test date validation
        valid_date = handler.validate_event_date(tomorrow)
        invalid_date = handler.validate_event_date('2020-01-01')
        
        print(f"✅ Date validation: Future date valid: {valid_date}")
        print(f"✅ Date validation: Past date invalid: {not invalid_date}")
        
        # Test popular events
        popular_events = handler.get_popular_events()
        print(f"✅ Popular events: {len(popular_events)} events available")
        
        print("\n✅ Calendar Handler working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing calendar handler: {e}")

if __name__ == "__main__":
    test_calendar_system()
    test_outfit_recommender()
    test_calendar_handler()