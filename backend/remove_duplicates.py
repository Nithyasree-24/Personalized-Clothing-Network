from db import execute_query

def remove_duplicate_products():
    """Remove duplicate products from api_cache table"""
    try:
        # Find duplicates based on product_id
        print("🔍 Checking for duplicate products...")
        
        duplicates = execute_query(
            """SELECT product_id, COUNT(*) as count 
               FROM api_cache 
               GROUP BY product_id 
               HAVING count > 1""",
            fetch=True
        )
        
        if not duplicates:
            print("✅ No duplicate products found!")
            return
        
        print(f"⚠️  Found {len(duplicates)} products with duplicates")
        
        # For each duplicate, keep only the most recent one
        for dup in duplicates:
            product_id = dup['product_id']
            count = dup['count']
            print(f"   - Product {product_id}: {count} duplicates")
            
            # Delete all but the most recent entry
            execute_query(
                """DELETE FROM api_cache 
                   WHERE product_id = %s 
                   AND id NOT IN (
                       SELECT id FROM (
                           SELECT id FROM api_cache 
                           WHERE product_id = %s 
                           ORDER BY cached_at DESC 
                           LIMIT 1
                       ) as keeper
                   )""",
                (product_id, product_id)
            )
        
        print("✅ Duplicates removed successfully!")
        
        # Show final count
        result = execute_query(
            "SELECT COUNT(*) as count FROM api_cache",
            fetch=True
        )
        total = result[0]['count'] if result else 0
        print(f"📊 Total unique products: {total}")
        
    except Exception as e:
        print(f"❌ Error removing duplicates: {e}")

if __name__ == "__main__":
    remove_duplicate_products()
