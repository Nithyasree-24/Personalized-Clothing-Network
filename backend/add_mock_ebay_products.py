"""
Add mock eBay products to database for testing
This allows you to see how the system works with eBay products without needing real product IDs
"""
from db import execute_query
import random

# Mock eBay products with realistic data
MOCK_EBAY_PRODUCTS = [
    # Women's Products
    {
        'product_id': 'ebay_women_001',
        'title': 'Women Floral Print Maxi Dress - Summer Collection',
        'price': 1299,
        'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_women_001',
        'rating': 4.5,
        'description': 'Beautiful floral print maxi dress perfect for summer occasions',
        'category': 'fashion',
        'gender': 'women',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_women_002',
        'title': 'Women Cotton Kurti with Palazzo Set',
        'price': 899,
        'image_url': 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_women_002',
        'rating': 4.3,
        'description': 'Comfortable cotton kurti with matching palazzo pants',
        'category': 'fashion',
        'gender': 'women',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_women_003',
        'title': 'Women Designer Saree with Blouse',
        'price': 2499,
        'image_url': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_women_003',
        'rating': 4.7,
        'description': 'Elegant designer saree with embroidered blouse piece',
        'category': 'fashion',
        'gender': 'women',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_women_004',
        'title': 'Women Denim Jacket - Casual Wear',
        'price': 1599,
        'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_women_004',
        'rating': 4.4,
        'description': 'Stylish denim jacket for casual outings',
        'category': 'fashion',
        'gender': 'women',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_women_005',
        'title': 'Women Formal Blazer - Office Wear',
        'price': 1899,
        'image_url': 'https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_women_005',
        'rating': 4.6,
        'description': 'Professional blazer perfect for office wear',
        'category': 'fashion',
        'gender': 'women',
        'source': 'ebay'
    },
    
    # Men's Products
    {
        'product_id': 'ebay_men_001',
        'title': 'Men Formal Shirt - Cotton Blend',
        'price': 799,
        'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_men_001',
        'rating': 4.4,
        'description': 'Premium cotton blend formal shirt for office wear',
        'category': 'fashion',
        'gender': 'men',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_men_002',
        'title': 'Men Slim Fit Jeans - Dark Blue',
        'price': 1299,
        'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_men_002',
        'rating': 4.5,
        'description': 'Comfortable slim fit jeans in dark blue wash',
        'category': 'fashion',
        'gender': 'men',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_men_003',
        'title': 'Men Leather Jacket - Winter Collection',
        'price': 3499,
        'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_men_003',
        'rating': 4.8,
        'description': 'Premium leather jacket for winter season',
        'category': 'fashion',
        'gender': 'men',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_men_004',
        'title': 'Men Sports T-Shirt - Gym Wear',
        'price': 599,
        'image_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_men_004',
        'rating': 4.3,
        'description': 'Breathable sports t-shirt for gym and fitness',
        'category': 'fashion',
        'gender': 'men',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_men_005',
        'title': 'Men Formal Blazer - Wedding Collection',
        'price': 2999,
        'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_men_005',
        'rating': 4.7,
        'description': 'Elegant formal blazer for weddings and parties',
        'category': 'fashion',
        'gender': 'men',
        'source': 'ebay'
    },
    
    # Kids Products
    {
        'product_id': 'ebay_kids_001',
        'title': 'Kids Cotton T-Shirt Set - Pack of 3',
        'price': 699,
        'image_url': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_kids_001',
        'rating': 4.5,
        'description': 'Comfortable cotton t-shirts for kids - pack of 3',
        'category': 'fashion',
        'gender': 'kids',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_kids_002',
        'title': 'Kids Party Dress - Girls',
        'price': 899,
        'image_url': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_kids_002',
        'rating': 4.6,
        'description': 'Beautiful party dress for girls',
        'category': 'fashion',
        'gender': 'kids',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_kids_003',
        'title': 'Kids Denim Shorts - Summer Wear',
        'price': 499,
        'image_url': 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_kids_003',
        'rating': 4.4,
        'description': 'Comfortable denim shorts for summer',
        'category': 'fashion',
        'gender': 'kids',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_kids_004',
        'title': 'Kids Winter Jacket - Warm & Cozy',
        'price': 1299,
        'image_url': 'https://images.unsplash.com/photo-1514090458221-65bb69cf63e6?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_kids_004',
        'rating': 4.7,
        'description': 'Warm winter jacket for kids',
        'category': 'fashion',
        'gender': 'kids',
        'source': 'ebay'
    },
    {
        'product_id': 'ebay_kids_005',
        'title': 'Kids School Uniform Set',
        'price': 799,
        'image_url': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=500',
        'product_url': 'https://www.ebay.in/itm/ebay_kids_005',
        'rating': 4.5,
        'description': 'Complete school uniform set for kids',
        'category': 'fashion',
        'gender': 'kids',
        'source': 'ebay'
    },
]

def add_mock_products():
    """Add mock eBay products to database"""
    added_count = 0
    skipped_count = 0
    
    print("🔄 Adding mock eBay products to database...")
    print("="*60)
    
    for product in MOCK_EBAY_PRODUCTS:
        try:
            # Check if product already exists
            existing = execute_query(
                "SELECT id FROM api_cache WHERE product_id = %s",
                (product['product_id'],),
                fetch=True
            )
            
            if existing:
                print(f"⏭️  Skipped: {product['title'][:50]}... (already exists)")
                skipped_count += 1
                continue
            
            # Insert product
            execute_query(
                """INSERT INTO api_cache 
                   (product_id, title, price, image_url, product_url, rating, description, category, gender, source) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    product['product_id'],
                    product['title'],
                    product['price'],
                    product['image_url'],
                    product['product_url'],
                    product['rating'],
                    product['description'],
                    product['category'],
                    product['gender'],
                    product['source']
                )
            )
            
            print(f"✅ Added: {product['title'][:50]}...")
            added_count += 1
            
        except Exception as e:
            print(f"❌ Error adding {product['title'][:30]}...: {e}")
    
    print("="*60)
    print(f"✅ Added {added_count} new mock eBay products")
    print(f"⏭️  Skipped {skipped_count} existing products")
    print(f"📦 Total: {added_count + skipped_count} products processed")
    
    # Show total count
    result = execute_query("SELECT COUNT(*) as count FROM api_cache", fetch=True)
    total = result[0]['count'] if result else 0
    print(f"💾 Total products in database: {total}")
    
    # Show breakdown by source
    sources = execute_query(
        "SELECT source, COUNT(*) as count FROM api_cache GROUP BY source",
        fetch=True
    )
    print("\nBreakdown by source:")
    for row in sources:
        print(f"   {row['source']}: {row['count']} products")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Mock eBay Products Generator")
    print("="*60)
    print("\nThis script adds mock eBay products to your database.")
    print("These are test products with realistic data but not from real eBay API.")
    print("\nUse this for:")
    print("  ✅ Testing the UI with more products")
    print("  ✅ Seeing how eBay products would look")
    print("  ✅ Development and demo purposes")
    print("\n" + "="*60 + "\n")
    
    add_mock_products()
    
    print("\n" + "="*60)
    print("✅ Done! Refresh your website to see the new products.")
    print("="*60)
