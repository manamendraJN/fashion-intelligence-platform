"""Quick test of the size manager"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from simple_size_manager import view_database, example_mens_tshirt

print("="*70)
print("TESTING SIZE CHART MANAGER")
print("="*70)

# First, view what's in the database
view_database()

# Ask if user wants to add examples
print("\n" + "="*70)
response = input("\nWould you like to add Nike Men's T-Shirt example? (y/n): ").strip().lower()
if response == 'y':
    example_mens_tshirt()
    print("\n✅ Example added! Viewing updated database...\n")
    view_database()
else:
    print("\nNo changes made. Exiting.")
