"""
Database connection and query handler for FashionPulse Chat Agent
"""
import pymysql
import logging
from typing import List, Dict, Optional, Any
from config import ChatAgentConfig

class DatabaseHandler:
    def __init__(self):
        self.config = ChatAgentConfig()
        self.connection = None
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = pymysql.connect(
                host=self.config.DB_HOST,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.logger.info("✅ Database connected successfully")
            return True
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("🔌 Database disconnected")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                self.logger.info(f"📊 Query executed: {len(results)} results found")
                return results
        except Exception as e:
            self.logger.error(f"❌ Query execution failed: {e}")
            return []
    
    def search_products(self, 
                       category: Optional[str] = None,
                       color: Optional[str] = None, 
                       gender: Optional[str] = None,
                       max_price: Optional[float] = None,
                       limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search products based on filters with exact keyword matching
        """
        # Base query - excluding stock information per user request
        query = f"""
        SELECT 
            product_id,
            product_name,
            product_category,
            product_description,
            color,
            size,
            gender,
            price,
            product_image
        FROM {self.config.DB_TABLE} 
        WHERE 1=1
        """
        
        params = []
        
        # Add category filter with exact matching
        if category:
            # Use exact matching for category to avoid showing t-shirts when searching for shirts
            category_lower = category.lower()
            if category_lower == 'shirts':
                # Only match "shirts" exactly, not "T-shirts"
                query += " AND product_category = 'shirts'"
            elif category_lower == 't-shirts':
                # Only match "T-shirts" exactly
                query += " AND product_category = 'T-shirts'"
            elif category_lower == 'dresses':
                query += " AND product_category = 'Dresses'"
            elif category_lower == 'bottom wear':
                query += " AND product_category = 'Bottom Wear'"
            elif category_lower == 'hoodies':
                query += " AND product_category = 'Hoodies'"
            elif category_lower == 'western wear':
                query += " AND product_category = 'Western Wear'"
            elif category_lower == 'ethnic wear':
                query += " AND product_category = 'Ethnic Wear'"
            elif category_lower == 'tops and co-ord sets':
                query += " AND product_category = 'Tops and Co-ord Sets'"
            elif category_lower == "women's bottomwear":
                query += " AND product_category = 'Women\\'s Bottomwear'"
            else:
                # Fallback to LIKE for other categories
                query += " AND LOWER(product_category) LIKE %s"
                params.append(f"%{category_lower}%")
        
        # Add color filter with exact matching
        if color:
            color_lower = color.lower()
            query += " AND LOWER(color) = %s"
            params.append(color_lower)
        
        # Add gender filter with exact matching
        if gender:
            gender_lower = gender.lower()
            if gender_lower in ['men', 'women', 'kids', 'unisex']:
                query += " AND LOWER(gender) = %s"
                params.append(gender_lower)
            else:
                # Fallback to LIKE for other gender values
                query += " AND LOWER(gender) LIKE %s"
                params.append(f"%{gender_lower}%")
        
        # Add price filter
        if max_price:
            query += " AND price <= %s"
            params.append(max_price)
        
        # Add ordering and limit
        query += " ORDER BY price ASC LIMIT %s"
        params.append(limit)
        
        self.logger.info(f"🔍 Exact keyword search with query: {query}")
        self.logger.info(f"📝 Parameters: {params}")
        
        return self.execute_query(query, tuple(params))
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get single product by ID"""
        query = f"SELECT * FROM {self.config.DB_TABLE} WHERE product_id = %s"
        results = self.execute_query(query, (product_id,))
        return results[0] if results else None
    
    def get_random_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get random products for suggestions"""
        query = f"""
        SELECT 
            product_id, product_name, price, color, gender, product_category
        FROM {self.config.DB_TABLE} 
        ORDER BY RAND() 
        LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        query = f"SELECT DISTINCT product_category FROM {self.config.DB_TABLE} ORDER BY product_category"
        results = self.execute_query(query)
        return [row['product_category'] for row in results]
    
    def get_colors(self) -> List[str]:
        """Get all unique colors"""
        query = f"SELECT DISTINCT color FROM {self.config.DB_TABLE} WHERE color IS NOT NULL ORDER BY color"
        results = self.execute_query(query)
        return [row['color'] for row in results]
    
    def get_price_range(self) -> Dict[str, float]:
        """Get min and max prices"""
        query = f"SELECT MIN(price) as min_price, MAX(price) as max_price FROM {self.config.DB_TABLE}"
        results = self.execute_query(query)
        if results:
            return {
                'min_price': float(results[0]['min_price'] or 0),
                'max_price': float(results[0]['max_price'] or 0)
            }
        return {'min_price': 0, 'max_price': 0}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        stats = {}
        
        # Total products
        query = f"SELECT COUNT(*) as total FROM {self.config.DB_TABLE}"
        result = self.execute_query(query)
        stats['total_products'] = result[0]['total'] if result else 0
        
        # Products by gender
        query = f"SELECT gender, COUNT(*) as count FROM {self.config.DB_TABLE} GROUP BY gender"
        results = self.execute_query(query)
        stats['by_gender'] = {row['gender']: row['count'] for row in results}
        
        # Price range
        stats['price_range'] = self.get_price_range()
        
        return stats