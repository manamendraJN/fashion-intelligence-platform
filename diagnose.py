"""
Quick diagnostic script to check if backend and database are working
"""

import sys
sys.path.append('backend')

print("=" * 60)
print("DIAGNOSTIC CHECK")
print("=" * 60)

# 1. Test database
try:
    import database
    items = database.get_all_wardrobe_items()
    print(f"✓ Database: {len(items)} items found")
    if items:
        print(f"  Sample: {items[0]['type']} (ID: {items[0]['id']})")
except Exception as e:
    print(f"✗ Database error: {e}")

# 2. Test color utils
try:
    from utils.color_utils import rgb_to_color_name
    test_color = rgb_to_color_name((0, 0, 255))
    print(f"✓ Color utils: Working (Blue = {test_color})")
except Exception as e:
    print(f"✗ Color utils error: {e}")

# 3. Test wardrobe routes import
try:
    from routes.wardrobe_routes import wardrobe_bp
    print(f"✓ Wardrobe routes: Imported successfully")
except Exception as e:
    print(f"✗ Wardrobe routes error: {e}")

# 4. Check if Flask app can be imported
try:
    from flask import Flask
    from flask_cors import CORS
    print(f"✓ Flask: Available")
except Exception as e:
    print(f"✗ Flask error: {e}")

print("=" * 60)
print("\nNEXT STEPS:")
print("1. Start backend: cd backend && python app.py")
print("2. Start frontend: cd frontend && npm run dev")
print("3. Open browser: http://localhost:5173")
print("=" * 60)
