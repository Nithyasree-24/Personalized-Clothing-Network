"""
Test script for FashionPulse Chat Agent
Tests various query types and validates responses
"""
import logging
from .chat_agent import FashionPulseChatAgent

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_chat_agent():
    """Test the chat agent with various queries"""
    
    print("🧪 Testing FashionPulse Chat Agent")
    print("="*50)
    
    # Test queries
    test_queries = [
        # Greeting
        "Hi there!",
        
        # Help
        "What can you help me with?",
        
        # Product searches
        "Show me red dresses under 2000",
        "Find jeans for men",
        "Looking for ethnic wear for women",
        "Blue shirts under 1500",
        "Show me black tops",
        "Find white sarees",
        
        # General queries
        "What categories do you have?",
        "Show me available colors",
        "What's your inventory stats?",
        
        # Edge cases
        "asdfgh",  # Random text
        "",  # Empty
        "Show me something expensive",
        "Find cheap clothes",
    ]
    
    # Initialize chat agent
    with FashionPulseChatAgent() as agent:
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. 💬 User: {query}")
            print("-" * 40)
            
            try:
                response = agent.process_message(query)
                print(f"🤖 Agent: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("-" * 40)
    
    print("\n🎉 Chat agent testing completed!")

def test_specific_product():
    """Test getting specific product details"""
    print("\n🔍 Testing specific product lookup...")
    
    with FashionPulseChatAgent() as agent:
        # Test with a known product ID
        response = agent.get_product_details("151")
        print(f"🤖 Product Details:\n{response}")

def test_database_connection():
    """Test database connection and basic queries"""
    print("\n🔌 Testing database connection...")
    
    with FashionPulseChatAgent() as agent:
        try:
            # Test stats
            stats = agent.db_handler.get_stats()
            print(f"📊 Database Stats: {stats}")
            
            # Test categories
            categories = agent.db_handler.get_categories()
            print(f"🏷️ Categories ({len(categories)}): {categories[:5]}...")
            
            # Test colors
            colors = agent.db_handler.get_colors()
            print(f"🎨 Colors ({len(colors)}): {colors[:10]}...")
            
            # Test search
            products = agent.db_handler.search_products(category="dress", limit=3)
            print(f"👗 Sample dresses: {len(products)} found")
            
        except Exception as e:
            print(f"❌ Database test error: {e}")

if __name__ == "__main__":
    # Run all tests
    test_database_connection()
    test_chat_agent()
    test_specific_product()