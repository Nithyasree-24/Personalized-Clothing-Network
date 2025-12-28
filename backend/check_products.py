from db import execute_query

print("\n" + "="*60)
print("Product Database Status")
print("="*60)

# Get breakdown by source and gender
result = execute_query(
    'SELECT source, gender, COUNT(*) as count FROM api_cache GROUP BY source, gender ORDER BY source, gender',
    fetch=True
)

print("\nProduct Breakdown:")
print("-"*60)
print(f"{'Source':<15} {'Gender':<15} {'Count':<10}")
print("-"*60)

for row in result:
    print(f"{row['source'].upper():<15} {row['gender']:<15} {row['count']:<10}")

# Get total
total = execute_query('SELECT COUNT(*) as count FROM api_cache', fetch=True)
print("-"*60)
print(f"{'TOTAL':<15} {'ALL':<15} {total[0]['count']:<10}")
print("="*60)

# Get sample products from each source
print("\nSample Products:")
print("="*60)

for source in ['amazon', 'ebay']:
    print(f"\n{source.upper()} Products (first 3):")
    print("-"*60)
    products = execute_query(
        f"SELECT title, price, gender FROM api_cache WHERE source = '{source}' LIMIT 3",
        fetch=True
    )
    for p in products:
        print(f"  • {p['title'][:50]}... (₹{p['price']}) [{p['gender']}]")

print("\n" + "="*60)
