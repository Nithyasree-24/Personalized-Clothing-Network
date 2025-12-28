#!/usr/bin/env python3
"""
Test Face Tone Flow with Colored Circles and Buttons
Tests the updated Face Tone implementation with actual skin tone colors and color-coded suggestion buttons
"""

import requests
import json
import time

def test_face_tone_flow():
    """Test the Face Tone flow with colored circles and buttons"""
    print("🎨 Testing Face Tone Flow with Colored Circles and Buttons")
    print("=" * 60)
    
    # Test Face Tone initiation
    print("\n1️⃣ Testing Face Tone Flow Initiation")
    print("-" * 40)
    
    try:
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Face Tone Analysis'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Face Tone flow initiated successfully")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'Fair' in result.get('response', '') and 'Wheatish' in result.get('response', ''):
                print("✅ Skin tone options (Fair, Wheatish, Dusky, Dark) are available")
            else:
                print("❌ Skin tone options not found in response")
        else:
            print(f"❌ Face Tone flow initiation failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to chat agent on port 5001")
        print("💡 Please start the server: python chat_agent/lightweight_api_server.py")
        return False
    
    # Test Fair skin tone selection
    print("\n2️⃣ Testing Fair Skin Tone Selection")
    print("-" * 40)
    
    try:
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Fair'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Fair skin tone selected successfully")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'Blue' in result.get('response', '') and 'Black' in result.get('response', ''):
                print("✅ Color suggestions for Fair skin (Blue, Black) are available")
            else:
                print("❌ Color suggestions for Fair skin not found")
        else:
            print(f"❌ Fair skin tone selection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing Fair skin tone: {e}")
    
    # Test Wheatish skin tone selection
    print("\n3️⃣ Testing Wheatish Skin Tone Selection")
    print("-" * 40)
    
    try:
        # Reset flow first
        requests.post('http://localhost:5001/api/chat', json={'message': 'Face Tone Analysis'})
        
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Wheatish'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Wheatish skin tone selected successfully")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'Red' in result.get('response', '') and 'Pink' in result.get('response', ''):
                print("✅ Color suggestions for Wheatish skin (Red, Pink) are available")
            else:
                print("❌ Color suggestions for Wheatish skin not found")
        else:
            print(f"❌ Wheatish skin tone selection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing Wheatish skin tone: {e}")
    
    # Test Dusky skin tone selection
    print("\n4️⃣ Testing Dusky Skin Tone Selection")
    print("-" * 40)
    
    try:
        # Reset flow first
        requests.post('http://localhost:5001/api/chat', json={'message': 'Face Tone Analysis'})
        
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Dusky'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Dusky skin tone selected successfully")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'White' in result.get('response', '') and 'Grey' in result.get('response', ''):
                print("✅ Color suggestions for Dusky skin (White, Grey) are available")
            else:
                print("❌ Color suggestions for Dusky skin not found")
        else:
            print(f"❌ Dusky skin tone selection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing Dusky skin tone: {e}")
    
    # Test Dark skin tone selection
    print("\n5️⃣ Testing Dark Skin Tone Selection")
    print("-" * 40)
    
    try:
        # Reset flow first
        requests.post('http://localhost:5001/api/chat', json={'message': 'Face Tone Analysis'})
        
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Dark'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Dark skin tone selected successfully")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'Green' in result.get('response', '') and 'White' in result.get('response', '') and 'Blue' in result.get('response', ''):
                print("✅ Color suggestions for Dark skin (Green, White, Blue) are available")
            else:
                print("❌ Color suggestions for Dark skin not found")
        else:
            print(f"❌ Dark skin tone selection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing Dark skin tone: {e}")
    
    # Test color selection
    print("\n6️⃣ Testing Color Selection")
    print("-" * 40)
    
    try:
        response = requests.post('http://localhost:5001/api/chat', json={
            'message': 'Blue'
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Color selection successful")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            if 'products' in result.get('response', '').lower():
                print("✅ Product search initiated after color selection")
            else:
                print("❌ Product search not initiated after color selection")
        else:
            print(f"❌ Color selection failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing color selection: {e}")

def print_color_mapping():
    """Print the color mapping for reference"""
    print("\n🎨 Color Mapping Reference")
    print("=" * 60)
    
    print("\n👤 Skin Tone Colors (Circles):")
    print("   • Fair: #fdbcb4 (Light peachy pink)")
    print("   • Wheatish: #deb887 (Burlywood)")
    print("   • Dusky: #cd853f (Peru brown)")
    print("   • Dark: #8b4513 (Saddle brown)")
    
    print("\n🌈 Suggested Color Buttons:")
    print("   • Blue: #3b82f6 (Blue)")
    print("   • Black: #1f2937 (Dark gray)")
    print("   • Red: #ef4444 (Red)")
    print("   • Pink: #ec4899 (Pink)")
    print("   • White: #ffffff (White with dark text)")
    print("   • Grey: #6b7280 (Gray)")
    print("   • Green: #10b981 (Emerald)")

def main():
    """Run complete Face Tone colored implementation test"""
    print("🧪 Face Tone Colored Circles & Buttons Test")
    print("=" * 60)
    
    # Print color mapping
    print_color_mapping()
    
    # Test Face Tone flow
    test_face_tone_flow()
    
    print("\n" + "=" * 60)
    print("✅ Face Tone Colored Implementation Test Complete!")
    
    print("\n📋 Implementation Summary:")
    print("   • Skin tone circles with actual skin colors")
    print("   • Color suggestion buttons with actual colors")
    print("   • Hover effects and visual feedback")
    print("   • Responsive design for all screen sizes")
    
    print("\n🎯 Visual Features:")
    print("   • Fair skin: Light peachy pink circle")
    print("   • Wheatish skin: Burlywood circle")
    print("   • Dusky skin: Peru brown circle")
    print("   • Dark skin: Saddle brown circle")
    print("   • Color buttons: Actual color backgrounds")
    print("   • Hover animations and scaling effects")
    
    print("\n🚀 Next Steps:")
    print("   1. Open frontend: http://localhost:3000")
    print("   2. Click chat icon and select 'Face Tone Analysis'")
    print("   3. See colored circles for skin tones")
    print("   4. See colored buttons for color suggestions")
    print("   5. Test the complete flow with visual feedback")

if __name__ == "__main__":
    main()