"""
Quick test to verify if products are being stored in database
"""
from api_cache_service import api_cache_service
from config import Config

print("\n" + "="*60)
print("🧪 QUICK PRODUCT STORAGE TEST")
print("="*60)

# Check API key
print("\n1. Checking API Key...")
if Config.RAPIDAPI_KEY and Config.RAPIDAPI_KEY != 'your-rapidapi-key-here':
    print(f"   ✅ API Key configured: {Config.RAPIDAPI_KEY[:10]}...")
else:
    print("   ⚠️  API Key NOT configured!")
    print("   Add your key to backend/.env file")
    exit()

# Check usage
print("\n2. Checking API Usage...")
stats = api_cache_service.get_usage_stats()
print(f"   Current: {stats['current_usage']}/{stats['monthly_limit']}")
print(f"   Remaining: {stats['remaining']}")
print(f"   Can make call: {'✅ Yes' if stats['can_make_call'] else '❌ No'}")

# Check cache
print("\n3. Checking Cached Products...")
cached = api_cache_service.get_cached_products(limit=5)
print(f"   Total cached: {len(cached)} products")

if len(cached) > 0:
    print("\n   Sample products:")
    for p in cached[:3]:
        print(f"   - {p['title'][:50]}... (${p['price']})")

# Offer to fetch
if stats['can_make_call']:
    print("\n4. Would you like to fetch fresh products from Amazon?")
    print("   This will use 1 API call and store products in database.")
    
    response = input("\n   Fetch products? (yes/no): ").lower()
    
    if response == 'yes':
        print("\n   🔄 Fetching products from Amazon API...")
        products = api_cache_service.fetch_from_amazon_api("men shirt", "fashion")
        
        if products:
            print(f"\n   ✅ Success! Fetched and stored {len(products)} products")
            print("\n   Sample products:")
            for p in products[:5]:
                print(f"   - {p['title'][:50]}...")
                print(f"     Price: ${p['price']}, Rating: {p['rating']}")
            
            # Show updated stats
            new_stats = api_cache_service.get_usage_stats()
            print(f"\n   📊 Updated Usage: {new_stats['current_usage']}/{new_stats['monthly_limit']}")
        else:
            print("\n   ❌ Failed to fetch products. Check your API key.")
    else:
        print("\n   Skipped fetching.")
else:
    print("\n4. ⚠️  API limit reached. Using cached products only.")

print("\n" + "="*60)
print("✅ Test Complete!")
print("="*60)
print("\nNext steps:")
print("1. Start backend: python app.py")
print("2. Start frontend: npm run dev")
print("3. Visit: http://localhost:3000/browse")
print("\n")
