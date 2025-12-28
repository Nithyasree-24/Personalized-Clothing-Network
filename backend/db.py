import pymysql
from config import Config

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
    except pymysql.Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        connection.close()
