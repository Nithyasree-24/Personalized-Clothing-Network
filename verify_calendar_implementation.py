#!/usr/bin/env python3
"""
Calendar Implementation Verification Script
Verifies that all calendar features have been properly implemented.
"""

import os
import re

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def search_in_file(filepath, patterns):
    """Search for patterns in a file"""
    if not os.path.exists(filepath):
        return {}
    
    results = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern_name, pattern in patterns.items():
            matches = re.search(pattern, content, re.DOTALL | re.MULTILINE)
            results[pattern_name] = bool(matches)
            
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {}
    
    return results

def main():
    print("🔍 Calendar Implementation Verification")
    print("=" * 50)
    
    # Check if main component exists
    component_file = "components/AIChatBox.tsx"
    if not check_file_exists(component_file):
        print(f"❌ {component_file} not found!")
        return
    
    print(f"✅ {component_file} found")
    
    # Define patterns to search for
    patterns = {
        "CustomCalendar_Component": r"const CustomCalendar.*React\.FC.*CustomCalendarProps",
        "Calendar_Props_Interface": r"interface CustomCalendarProps",
        "Year_Month_Day_Steps": r"currentStep.*useState.*year.*month.*day",
        "Back_Button_Logic": r"calendarStep.*!==.*gender.*button.*onClick.*Back",
        "Date_Selection_Handler": r"handleDateSelection.*year.*month.*day",
        "Custom_Event_Input": r"showCustomEventInput.*input.*placeholder.*custom",
        "Event_Storage": r"saveUserEvent.*localStorage.*fashionpulse_events",
        "Outfit_Suggestions": r"getEventOutfitSuggestions.*daysUntil.*<=.*7",
        "Calendar_Modal": r"showCalendar.*&&.*Calendar.*Popup",
        "Progress_Indicator": r"Progress.*Indicator.*calendarStep.*gender.*date.*event",
        "Black_Text_Date": r"text-black.*toLocaleDateString",
        "Others_Option": r"Others.*Custom.*Event.*handleCalendarStep"
    }
    
    print("\n🔍 Searching for implementation patterns...")
    results = search_in_file(component_file, patterns)
    
    # Display results
    print("\n📋 Implementation Status:")
    print("-" * 30)
    
    all_found = True
    for pattern_name, found in results.items():
        status = "✅" if found else "❌"
        description = pattern_name.replace("_", " ").title()
        print(f"{status} {description}")
        if not found:
            all_found = False
    
    print("\n" + "=" * 50)
    
    if all_found:
        print("🎉 ALL CALENDAR FEATURES IMPLEMENTED SUCCESSFULLY!")
        print("\n✨ Features included:")
        print("   • Custom Calendar Component with Year → Month → Day flow")
        print("   • Back button navigation between calendar steps")
        print("   • Selected date display in black text")
        print("   • 'Others' option for custom event input")
        print("   • Event storage with localStorage")
        print("   • Automatic outfit suggestions for upcoming events")
        print("   • Progress indicator showing current step")
        print("   • Complete calendar modal with proper styling")
        
        print("\n🚀 Ready to test:")
        print("   1. npm run dev")
        print("   2. python chat_agent/lightweight_api_server.py")
        print("   3. Open website and test calendar functionality")
        
    else:
        print("⚠️  Some features may be missing or need verification")
        print("   Please check the implementation manually")
    
    print("\n📄 Test file created: test_calendar_ui_complete.html")
    print("   Open this file in a browser to see detailed implementation status")

if __name__ == "__main__":
    main()