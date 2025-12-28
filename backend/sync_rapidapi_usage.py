from db import execute_query
from datetime import datetime

def sync_rapidapi_usage(actual_count):
    """
    Manually sync the API usage count with RapidAPI dashboard
    
    Args:
        actual_count: The actual number shown in RapidAPI dashboard
    """
    try:
        month_year = datetime.now().strftime('%Y-%m')
        
        # Check if record exists
        existing = execute_query(
            "SELECT id, request_count FROM api_usage WHERE api_name = 'amazon' AND month_year = %s",
            (month_year,),
            fetch=True
        )
        
        if existing:
            old_count = existing[0]['request_count']
            # Update to actual count
            execute_query(
                "UPDATE api_usage SET request_count = %s, last_request = NOW() WHERE api_name = 'amazon' AND month_year = %s",
                (actual_count, month_year)
            )
            print(f"✅ Updated API usage: {old_count} → {actual_count}")
        else:
            # Insert new record
            execute_query(
                "INSERT INTO api_usage (api_name, endpoint, request_count, month_year, last_request) VALUES (%s, %s, %s, %s, NOW())",
                ('amazon', 'real-time-amazon-data', actual_count, month_year)
            )
            print(f"✅ Created new API usage record: {actual_count} calls")
        
        # Show current stats
        result = execute_query(
            "SELECT request_count FROM api_usage WHERE api_name = 'amazon' AND month_year = %s",
            (month_year,),
            fetch=True
        )
        
        if result:
            current = result[0]['request_count']
            remaining = 100 - current
            percentage = (current / 100) * 100
            
            print(f"\n📊 Current Stats:")
            print(f"   Used: {current}/100")
            print(f"   Remaining: {remaining}")
            print(f"   Percentage: {percentage:.1f}%")
            
    except Exception as e:
        print(f"❌ Error syncing usage: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sync_rapidapi_usage.py <actual_count>")
        print("Example: python sync_rapidapi_usage.py 36")
        sys.exit(1)
    
    try:
        actual_count = int(sys.argv[1])
        sync_rapidapi_usage(actual_count)
    except ValueError:
        print("❌ Error: Please provide a valid number")
        sys.exit(1)
