"""Show where tolerance and weights are configured"""

print("\n" + "="*70)
print("TOLERANCE AND WEIGHTS CONFIGURATION LOCATIONS")
print("="*70)

print("\n📍 LOCATION 1: Base Tolerance & Weight")
print("-" * 70)
print("File: backend/database/db_manager.py")
print("Function: get_sizes_for_chart()")
print("Lines: 271-274")
print()
print("Code:")
print("    'optimal': (min_val + max_val) / 2,")
print("    'tolerance': 2.0,  # ← DEFAULT TOLERANCE (2 cm)")
print("    'weight': 1.0      # ← BASE WEIGHT")
print()
print("💡 What this does:")
print("   • Sets 2.0 cm tolerance for ALL measurements")
print("   • Sets base weight of 1.0 (gets multiplied by importance weight)")
print()
print("✏️  To modify:")
print("   • Change 2.0 to any value (e.g., 3.0 for more flexible sizing)")
print()

print("\n📍 LOCATION 2: Category Importance Weights")
print("-" * 70)
print("File: backend/database/db_manager.py")
print("Function: get_category_measurement_requirements()")
print("Lines: 310-370")
print()
print("Code:")
print("    if 't-shirt' in category_name:")
print("        return [")
print("            {'measurement_type': 'chest', 'importance_weight': 1.0, ...},")
print("            {'measurement_type': 'shoulder_breadth', 'importance_weight': 0.8, ...},")
print("            {'measurement_type': 'waist', 'importance_weight': 0.6, ...}")
print("        ]")
print()
print("💡 What this does:")
print("   • Chest gets 1.0 weight (most important)")
print("   • Shoulder gets 0.8 weight (important)")
print("   • Waist gets 0.6 weight (less important)")
print()
print("✏️  To modify:")
print("   • Change importance_weight values (0.0 - 1.0)")
print("   • Add new categories or measurements")
print()

print("\n🧮 FINAL CALCULATION")
print("-" * 70)
print("Final Weight = base_weight × importance_weight")
print()
print("Examples:")
print("   T-Shirt Chest:    1.0 × 1.0 = 1.0 (highest impact)")
print("   T-Shirt Shoulder: 1.0 × 0.8 = 0.8 (high impact)")
print("   T-Shirt Waist:    1.0 × 0.6 = 0.6 (medium impact)")
print()
print("   Shorts Waist:     1.0 × 1.0 = 1.0 (highest impact)")
print("   Shorts Hip:       1.0 × 0.9 = 0.9 (high impact)")
print("   Shorts Leg:       1.0 × 0.5 = 0.5 (low impact)")
print()

print("\n📊 ALL CATEGORY WEIGHTS")
print("-" * 70)
categories = {
    "T-Shirt/Polo": [("chest", 1.0), ("shoulder", 0.8), ("waist", 0.6)],
    "Shirt": [("chest", 1.0), ("shoulder", 0.8), ("sleeve", 0.7), ("waist", 0.6)],
    "Hoodie": [("chest", 1.0), ("shoulder", 0.8), ("waist", 0.7)],
    "Sweater": [("chest", 1.0), ("shoulder", 0.8), ("sleeve", 0.7), ("waist", 0.7)],
    "Shorts": [("waist", 1.0), ("hip", 0.9), ("leg", 0.5)],
    "Jeans/Pants": [("waist", 1.0), ("hip", 0.9), ("leg", 0.7)],
    "Dress/Skirt": [("chest", 1.0), ("waist", 1.0), ("hip", 0.9)],
    "Jacket": [("chest", 1.0), ("shoulder", 0.9), ("arm", 0.8)],
}

for cat, measurements in categories.items():
    print(f"\n{cat}:")
    for meas, weight in measurements:
        print(f"   • {meas:12} : {weight}")

print("\n" + "="*70)
print("📖 See docs/TOLERANCE_AND_WEIGHTS_CONFIGURATION.md for details")
print("="*70)
