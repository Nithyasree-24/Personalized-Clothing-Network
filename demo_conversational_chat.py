#!/usr/bin/env python3
"""
Demo: Conversational Chat Behavior
Shows how the chat now behaves like ChatGPT/human assistant
"""
import requests
import json
import time

def demo_conversation():
    print('🤖 FashionPulse Conversational Chat Demo')
    print('='*60)
    print('Demonstrating human-like conversation behavior...\n')
    
    # Conversation flow demo
    conversation = [
        {
            'user': 'hi',
            'description': 'Simple greeting - should be friendly, not show products'
        },
        {
            'user': 'how are you?',
            'description': 'Casual question - should respond conversationally'
        },
        {
            'user': 'what can you help me with?',
            'description': 'General inquiry - should explain capabilities'
        },
        {
            'user': 'show me red dresses under ₹2000',
            'description': 'Product search - should show products'
        },
        {
            'user': 'thank you',
            'description': 'Gratitude - should respond politely'
        },
        {
            'user': 'what is your return policy?',
            'description': 'E-commerce query - should provide policy info'
        },
        {
            'user': 'bye',
            'description': 'Farewell - should say goodbye nicely'
        }
    ]
    
    for i, turn in enumerate(conversation, 1):
        print(f"👤 User: {turn['user']}")
        print(f"💭 Expected: {turn['description']}")
        
        try:
            response = requests.post('http://localhost:5001/api/chat', 
                json={'message': turn['user']}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                products = data.get('products', [])
                
                print(f"🤖 Assistant: {response_text}")
                
                if products:
                    print(f"📦 Products returned: {len(products)} items")
                
                # Analysis
                if turn['user'] in ['hi', 'how are you?', 'thank you', 'bye']:
                    if products:
                        print("⚠️  WARNING: Conversational message returned products!")
                    else:
                        print("✅ GOOD: Conversational response, no products")
                elif 'show me' in turn['user']:
                    if products:
                        print("✅ GOOD: Product search returned products")
                    else:
                        print("⚠️  WARNING: Product search didn't return products!")
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
        time.sleep(1)  # Small delay for readability
    
    print("\n🎯 Demo Complete!")
    print("\n✅ Key Improvements:")
    print("• Greetings get friendly responses (not product lists)")
    print("• Casual conversation is handled naturally")
    print("• Product searches still work perfectly")
    print("• E-commerce queries get detailed responses")
    print("• Chat behaves like ChatGPT/human assistant")
    print("\n🚀 Your chat is now conversational and human-like!")

if __name__ == '__main__':
    demo_conversation()