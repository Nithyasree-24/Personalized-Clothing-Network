#!/usr/bin/env python3
"""
Test Enhanced Chat Agent with Policy Support
Tests all types of queries including orders, returns, cancellations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'chat_agent'))

from chat_agent.lightweight_chat_agent import LightweightFashionPulseChatAgent

def test_chat_agent():
    """Test the enhanced chat agent with various query types"""
    
    print("🤖 Testing Enhanced FashionPulse Chat Agent")
    print("=" * 50)
    
    # Initialize chat agent
    agent = LightweightFashionPulseChatAgent()
    
    # Test queries
    test_queries = [
        # Greetings
        "Hi there!",
        "Good morning",
        
        # Product searches
        "Show me red dresses",
        "Find jeans under 2000",
        "I want blue shirts for men",
        
        # Policy queries
        "What's your return policy?",
        "How can I cancel my order?",
        "Tell me about shipping",
        "What are the delivery charges?",
        "How do I return an item?",
        "Can I get a refund?",
        
        # Order queries
        "Track my order",
        "Where is my order #FP12345?",
        "Order status",
        
        # General e-commerce
        "What payment methods do you accept?",
        "Do you have size guide?",
        "How long does delivery take?",
        "Customer support contact",
        
        # Conversational
        "Thank you",
        "That's great!",
        "How are you?",
        "Goodbye"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. 💬 User: {query}")
        print("-" * 30)
        
        try:
            response = agent.process_message(query)
            print(f"🤖 Bot: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("✅ Chat agent testing completed!")
    
    # Test LLM status
    print("\n📊 LLM Status:")
    status = agent.get_llm_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Close agent
    agent.close()

if __name__ == "__main__":
    test_chat_agent()