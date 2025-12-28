# RapidAPI Usage Sync Guide

## How to Sync API Request Count

The API usage counter on the website shows the number of requests made to RapidAPI. To keep it accurate, you need to manually sync it with the RapidAPI dashboard.

### Steps to Sync:

1. **Check RapidAPI Dashboard**
   - Go to https://rapidapi.com/developer/dashboard
   - Find your "Real-Time Amazon Data" API
   - Note the "API Calls" number (e.g., 36)

2. **Run Sync Script**
   ```bash
   cd backend
   python sync_rapidapi_usage.py <actual_count>
   ```
   
   Example:
   ```bash
   python sync_rapidapi_usage.py 36
   ```

3. **Verify Update**
   - The script will show the old and new counts
   - Check the website counter (top-right corner)
   - It should now match the RapidAPI dashboard

### Current Status:
- **Used:** 36/100 requests
- **Remaining:** 64 requests
- **Percentage:** 36%
- **Status:** 🟢 Green (under 70%)

### Auto-Refresh:
The counter on the website automatically refreshes every **5 seconds** to show real-time updates.

### Manual Refresh:
Click the refresh icon (🔄) on the counter to update immediately.

### When to Sync:
- After making API calls from the website
- When you notice the count doesn't match RapidAPI dashboard
- At the start of each day to ensure accuracy
- Before making new API calls to check remaining quota

### Notes:
- RapidAPI doesn't provide an API to fetch usage statistics automatically
- Manual sync is required to keep the counter accurate
- The counter tracks usage per month (resets monthly)
- Monthly limit: 100 requests
