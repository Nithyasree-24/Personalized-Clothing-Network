#!/usr/bin/env python3
"""
Clothing API Service
Service to fetch products from the clothing table with proper column mapping
"""

from db import execute_query

class ClothingAPIService:
    def __init__(self):
        pass
    
    def get_clothing_products(self, category=None, gender=None, limit=500, search_query=None):
        """Get products from clothing table with flexible search"""
        try:
            # Map clothing table columns to expected API format
            query = """
            SELECT 
                product_id,
                product_name as title,
                price,
                product_image as image_url,
                product_category as category,
                gender,
                product_description as description,
                color,
                size,
                stock,
                created_at
            FROM clothing 
            WHERE 1=1
            """
            params = []
            
            print(f"DEBUG: get_clothing_products called - category={category}, gender={gender}, search_query={search_query}")
            
            # Flexible search across title, category, gender, description
            if search_query:
                search_terms = search_query.lower().split()
                search_conditions = []
                for term in search_terms:
                    search_conditions.append(
                        "(LOWER(product_name) LIKE %s OR LOWER(product_category) LIKE %s OR LOWER(gender) LIKE %s OR LOWER(product_description) LIKE %s)"
                    )
                    search_pattern = f"%{term}%"
                    params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
                
                if search_conditions:
                    query += " AND (" + " OR ".join(search_conditions) + ")"
            
            # Apply filters only when no search query (for category endpoints)
            if not search_query:
                # Handle special "All" categories
                if category == "All Women":
                    query += " AND LOWER(gender) = %s"
                    params.append("women")
                elif category == "All Men":
                    query += " AND LOWER(gender) = %s"
                    params.append("men")
                elif category:
                    # For specific categories, match exact category name
                    query += " AND LOWER(product_category) = %s"
                    params.append(category.lower())
                
                if gender and category not in ["All Women", "All Men"]:
                    query += " AND LOWER(gender) = %s"
                    params.append(gender.lower())
            
            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)
            
            print(f"DEBUG: Final query: {query}")
            print(f"DEBUG: Final params: {params}")
            
            products = execute_query(query, tuple(params), fetch=True)
            
            # Transform products to match expected format
            if products:
                transformed_products = []
                for product in products:
                    transformed_product = {
                        'product_id': str(product['product_id']),
                        'id': product['product_id'],
                        'title': product['title'],
                        'price': float(product['price']),
                        'image_url': product['image_url'],
                        'category': product['category'],
                        'gender': product['gender'].lower() if product['gender'] else 'unisex',
                        'description': product['description'] or '',
                        'color': product['color'] or '',
                        'size': product['size'] or '',
                        'stock': product['stock'] or 0,
                        'rating': 4.5,  # Default rating
                        'source': 'clothing_table',
                        'cached_at': product['created_at'].isoformat() if product['created_at'] else ''
                    }
                    transformed_products.append(transformed_product)
                
                print(f"DEBUG: Returning {len(transformed_products)} clothing products")
                return transformed_products
            
            print(f"DEBUG: No products found")
            return []
            
        except Exception as e:
            print(f"Database error in get_clothing_products: {e}")
            return []
    
    def get_products(self, query, category='fashion', use_cache_first=True):
        """
        Get products from clothing table - main entry point
        """
        # For generic queries, return all products
        if query.lower() in ['clothing fashion', 'fashion', 'clothing']:
            products = self.get_clothing_products(limit=500)
            if products:
                print(f"📦 Returning ALL {len(products)} products from clothing table")
                return products
        else:
            products = self.get_clothing_products(search_query=query, limit=500)
            if products:
                print(f"📦 Returning {len(products)} products from clothing table for query: {query}")
                return products
        
        print("⚠️ No products found in clothing table")
        return []
    
    def get_cached_products(self, category=None, gender=None, limit=500, search_query=None):
        """Alias for get_clothing_products to maintain compatibility"""
        return self.get_clothing_products(category, gender, limit, search_query)

# Singleton instance
clothing_api_service = ClothingAPIService()