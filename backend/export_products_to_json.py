import json
from db import execute_query

def export_products():
    """Export all products from database to JSON file"""
    try:
        products = execute_query(
            "SELECT * FROM api_cache ORDER BY cached_at DESC",
            fetch=True
        )
        
        if products:
            # Convert datetime objects to strings
            for product in products:
                if 'cached_at' in product and product['cached_at']:
                    product['cached_at'] = str(product['cached_at'])
            
            with open('fallback_products.json', 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(products)} products to fallback_products.json")
        else:
            print("⚠️  No products found in database")
            
    except Exception as e:
        print(f"❌ Error exporting products: {e}")

if __name__ == "__main__":
    export_products()
