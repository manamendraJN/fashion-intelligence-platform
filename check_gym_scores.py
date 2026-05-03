"""Check which items have Gym event scores"""
import sys
sys.path.append('backend')
import database

items = database.get_all_wardrobe_items()

print(f"Total items in database: {len(items)}\n")

# Items with high Gym scores
gym_items = [
    {
        'id': i['id'], 
        'type': i['type'], 
        'color': i.get('primaryColor', 'Unknown'),
        'gym_score': i.get('eventScores', {}).get('Gym', 0)
    } 
    for i in items 
    if i.get('eventScores', {}).get('Gym', 0) > 0.5
]

print(f"Items with Gym score > 0.5: {len(gym_items)}")
for item in gym_items[:15]:
    print(f"  - ID {item['id']}: {item['type']} ({item['color']}) - Gym score: {item['gym_score']:.2f}")

# Let's also check Office scores for these items
print("\n" + "="*60)
print("Checking Office scores for Pencil Skirts:")
pencil_skirts = [i for i in items if 'pencil' in i.get('type', '').lower()]
for item in pencil_skirts[:5]:
    gym_score = item.get('eventScores', {}).get('Gym', 0)
    office_score = item.get('eventScores', {}).get('Office', 0)
    print(f"  - ID {item['id']}: {item['type']}")
    print(f"      Gym: {gym_score:.2f}, Office: {office_score:.2f}")
