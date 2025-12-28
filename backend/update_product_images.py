"""
Update product images to match product titles and categories
Uses appropriate Unsplash images for each product type
"""
from db import execute_query

# Category-specific image mappings
IMAGE_MAPPINGS = {
    # Women's Products
    "dress": [
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500",  # Maxi dress
        "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500",  # Party dress
        "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500",  # Casual dress
        "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=500",  # Midi dress
        "https://images.unsplash.com/photo-1612423284934-2850a4ea6b0f?w=500",  # Bodycon dress
    ],
    "kurti": [
        "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",  # Traditional kurti
        "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500",  # Cotton kurti
        "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500",  # Ethnic kurti
    ],
    "top": [
        "https://images.unsplash.com/photo-1564257577-d18b7c1a4b8f?w=500",  # Casual top
        "https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=500",  # Crop top
        "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500",  # Tank top
        "https://images.unsplash.com/photo-1618932260643-eee4a2f652a6?w=500",  # Blouse
    ],
    "women_bottom": [
        "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",  # Jeans
        "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500",  # Palazzo
        "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=500",  # Trousers
        "https://images.unsplash.com/photo-1624206112918-f140f087f9b5?w=500",  # Leggings
    ],
    "saree": [
        "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",  # Designer saree
        "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500",  # Traditional saree
        "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500",  # Ethnic saree
    ],
    "ethnic_women": [
        "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",  # Anarkali
        "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500",  # Salwar
        "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500",  # Lehenga
        "https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=500",  # Ethnic wear
    ],
    "women_jacket": [
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",  # Denim jacket
        "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500",  # Blazer
        "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500",  # Leather jacket
        "https://images.unsplash.com/photo-1548126032-079d4823e5d2?w=500",  # Cardigan
    ],
    
    # Men's Products
    "men_shirt": [
        "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500",  # Formal shirt
        "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500",  # Casual shirt
        "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=500",  # Denim shirt
        "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=500",  # Linen shirt
    ],
    "men_tshirt": [
        "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500",  # Basic t-shirt
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",  # Polo shirt
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500",  # V-neck
        "https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=500",  # Graphic tee
    ],
    "men_bottom": [
        "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500",  # Jeans
        "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500",  # Trousers
        "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500",  # Chinos
        "https://images.unsplash.com/photo-1555689502-c4b22d76c56f?w=500",  # Cargo pants
    ],
    "men_ethnic": [
        "https://images.unsplash.com/photo-1626497764746-6dc36546b388?w=500",  # Kurta
        "https://images.unsplash.com/photo-1605518216938-7c31b7b14ad0?w=500",  # Sherwani
        "https://images.unsplash.com/photo-1622124358620-e45a1e3c5b5e?w=500",  # Pathani
        "https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?w=500",  # Nehru jacket
    ],
    "men_jacket": [
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500",  # Leather jacket
        "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500",  # Denim jacket
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500",  # Blazer
        "https://images.unsplash.com/photo-1548126032-079d4823e5d2?w=500",  # Hoodie
    ],
    
    # Kids Products
    "girls": [
        "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=500",  # Girls dress
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500",  # Girls casual
        "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500",  # Girls ethnic
        "https://images.unsplash.com/photo-1514090458221-65bb69cf63e6?w=500",  # Girls jacket
    ],
    "boys": [
        "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=500",  # Boys shirt
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500",  # Boys casual
        "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500",  # Boys ethnic
        "https://images.unsplash.com/photo-1514090458221-65bb69cf63e6?w=500",  # Boys jacket
    ],
    "kids_unisex": [
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500",  # Kids wear
        "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500",  # Kids casual
        "https://images.unsplash.com/photo-1514090458221-65bb69cf63e6?w=500",  # Kids jacket
        "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=500",  # Kids party
    ],
}

def categorize_product(title):
    """Determine the image category based on product title"""
    title_lower = title.lower()
    
    # Women's categories
    if "dress" in title_lower:
        return "dress"
    elif "kurti" in title_lower or "kurta" in title_lower:
        return "kurti"
    elif "saree" in title_lower:
        return "saree"
    elif any(word in title_lower for word in ["anarkali", "salwar", "lehenga", "sharara", "palazzo suit", "ethnic"]):
        return "ethnic_women"
    elif any(word in title_lower for word in ["top", "blouse", "crop", "tank", "tunic", "peplum"]):
        return "top"
    elif any(word in title_lower for word in ["palazzo", "jeans", "legging", "trouser", "short", "culotte", "pant", "jogger", "capri", "cargo"]) and "women" in title_lower:
        return "women_bottom"
    elif any(word in title_lower for word in ["jacket", "blazer", "cardigan", "coat", "shrug", "windcheater", "hoodie", "bomber", "puffer"]) and "women" in title_lower:
        return "women_jacket"
    
    # Men's categories
    elif "shirt" in title_lower and "men" in title_lower and "t-shirt" not in title_lower:
        return "men_shirt"
    elif "t-shirt" in title_lower or "tshirt" in title_lower or ("polo" in title_lower and "men" in title_lower):
        return "men_tshirt"
    elif any(word in title_lower for word in ["jeans", "trouser", "chino", "cargo", "jogger", "short", "track pant", "pant"]) and "men" in title_lower:
        return "men_bottom"
    elif any(word in title_lower for word in ["kurta", "sherwani", "pathani", "nehru", "dhoti", "indo-western", "bandhgala", "jodhpuri"]):
        return "men_ethnic"
    elif any(word in title_lower for word in ["jacket", "blazer", "hoodie", "sweater", "cardigan", "coat", "windcheater", "bomber", "puffer"]) and "men" in title_lower:
        return "men_jacket"
    
    # Kids categories
    elif "girls" in title_lower:
        return "girls"
    elif "boys" in title_lower:
        return "boys"
    elif "kids" in title_lower:
        return "kids_unisex"
    
    # Default
    return "dress"

def update_images():
    """Update all eBay product images with appropriate category-specific images"""
    
    print("\n" + "="*70)
    print("Updating Product Images to Match Titles")
    print("="*70)
    
    # Get all eBay products
    products = execute_query(
        "SELECT id, product_id, title FROM api_cache WHERE source = 'ebay' ORDER BY id",
        fetch=True
    )
    
    if not products:
        print("No eBay products found!")
        return
    
    print(f"\nFound {len(products)} eBay products to update")
    print("-"*70)
    
    updated_count = 0
    category_counts = {}
    
    for product in products:
        try:
            product_id = product['product_id']
            title = product['title']
            
            # Determine category
            category = categorize_product(title)
            
            # Get appropriate image
            images = IMAGE_MAPPINGS.get(category, IMAGE_MAPPINGS["dress"])
            image_url = images[updated_count % len(images)]
            
            # Update image
            execute_query(
                "UPDATE api_cache SET image_url = %s WHERE product_id = %s",
                (image_url, product_id)
            )
            
            # Track statistics
            category_counts[category] = category_counts.get(category, 0) + 1
            updated_count += 1
            
            print(f"✅ {title[:60]}...")
            print(f"   Category: {category} | Image: {image_url[:50]}...")
            
        except Exception as e:
            print(f"❌ Error updating {title[:30]}...: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Successfully updated {updated_count} product images")
    print("="*70)
    
    # Show category breakdown
    print("\n📊 Images Updated by Category:")
    print("-"*70)
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {category:20} : {count:3} products")
    
    print("\n" + "="*70)
    print("🎉 All product images now match their titles!")
    print("="*70)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Product Image Updater")
    print("="*70)
    print("\nThis will update all eBay product images to match their titles.")
    print("Each product will get an appropriate category-specific image.")
    print("\n" + "="*70 + "\n")
    
    update_images()
    
    print("\n✅ Done! Refresh your website to see the updated images.")
    print("🌐 Visit: http://localhost:3000/home\n")
