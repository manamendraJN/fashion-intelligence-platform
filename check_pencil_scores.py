import sqlite3
import json

conn = sqlite3.connect('backend/fashion_wardrobe.db')
cursor = conn.cursor()

# Check pencil skirts
cursor.execute("SELECT id, clothing_type, event_scores, best_event FROM wardrobe_items WHERE id IN (249, 250, 251, 252, 253)")
pencil_skirts = cursor.fetchall()

print(f"\n{'='*70}")
print(f"PENCIL SKIRT EVENT SCORES:")
print(f"{'='*70}\n")

for item_id, clothing_type, scores_json, best_event in pencil_skirts:
    scores = json.loads(scores_json)
    print(f"ID {item_id}: {clothing_type}")
    print(f"  Best Event (DB): {best_event}")
    print(f"  Office Score: {scores.get('Office', scores.get('Office Meeting', 'N/A'))}")
    print(f"  Casual Score: {scores.get('Casual', scores.get('Casual Outing', 'N/A'))}")
    print()

conn.close()
