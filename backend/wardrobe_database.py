"""
SQLite Database module for Fashion Intelligence Platform
Stores wardrobe items and user profile data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path(__file__).parent / 'fashion_wardrobe.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Wardrobe items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wardrobe_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            image_path TEXT NOT NULL,
            clothing_type TEXT,
            confidence REAL,
            top_5 TEXT,
            event_scores TEXT,
            best_event TEXT,
            primary_color TEXT,
            color_rgb TEXT,
            all_colors TEXT,
            wear_count INTEGER DEFAULT 0,
            last_worn TEXT,
            wear_history TEXT DEFAULT '[]',
            is_favorite INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add color columns if they don't exist (migration)
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'primary_color' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN primary_color TEXT')
    if 'color_rgb' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN color_rgb TEXT')
    if 'all_colors' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN all_colors TEXT')
    
    # Add analytics columns for advanced features
    if 'purchase_price' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN purchase_price REAL')
    if 'purchase_date' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN purchase_date TEXT')
    if 'season' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN season TEXT')
    
    # User profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            style_preferences TEXT DEFAULT '{}',
            total_interactions INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default user profile if not exists
    cursor.execute('SELECT id FROM user_profile WHERE id = 1')
    if not cursor.fetchone():
        default_profile = {
            'casual': 0, 
            'formal': 0, 
            'sporty': 0, 
            'trendy': 0,
            'classic': 0, 
            'bohemian': 0, 
            'minimalist': 0
        }
        cursor.execute('''
            INSERT INTO user_profile (id, style_preferences, total_interactions, updated_at)
            VALUES (1, ?, 0, ?)
        ''', (
            json.dumps(default_profile),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully")

def add_wardrobe_item(filename, image_path, clothing_type, confidence, top_5, event_scores, best_event, 
                      primary_color=None, color_rgb=None, all_colors=None):
    """Add a new wardrobe item to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO wardrobe_items (
            filename, image_path, clothing_type, confidence, 
            top_5, event_scores, best_event, primary_color, color_rgb, all_colors,
            wear_count, last_worn, wear_history, is_favorite, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, '[]', 0, ?)
    ''', (
        filename,
        image_path,
        clothing_type,
        confidence,
        json.dumps(top_5),
        json.dumps(event_scores),
        best_event,
        primary_color,
        json.dumps(color_rgb) if color_rgb else None,
        json.dumps(all_colors) if all_colors else None,
        datetime.now().isoformat()
    ))
    
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Added wardrobe item: {filename} (ID: {item_id})")
    return item_id

def get_all_wardrobe_items():
    """Get all wardrobe items"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure is_disliked column exists
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'is_disliked' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN is_disliked INTEGER DEFAULT 0')
        conn.commit()
    
    cursor.execute('SELECT * FROM wardrobe_items ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for row in rows:
        try:
            # Check if is_disliked column exists
            is_disliked = False
            if 'is_disliked' in row.keys():
                is_disliked = bool(row['is_disliked'])
            
            # Safely get color fields
            color_rgb = None
            if 'color_rgb' in row.keys() and row['color_rgb']:
                try:
                    color_rgb = json.loads(row['color_rgb'])
                except:
                    pass
            
            all_colors = []
            if 'all_colors' in row.keys() and row['all_colors']:
                try:
                    all_colors = json.loads(row['all_colors'])
                except:
                    pass
            
            items.append({
                'id': row['id'],
                'filename': row['filename'],
                'url': row['image_path'],
                'type': row['clothing_type'],
                'confidence': row['confidence'],
                'primaryColor': row['primary_color'] if 'primary_color' in row.keys() else None,
                'colorRgb': color_rgb,
                'allColors': all_colors,
                'top5': json.loads(row['top_5']) if row['top_5'] else [],
                'eventScores': json.loads(row['event_scores']) if row['event_scores'] else {},
                'bestEvent': row['best_event'],
                'wearCount': row['wear_count'],
                'lastWorn': row['last_worn'],
                'wearHistory': json.loads(row['wear_history']) if row['wear_history'] else [],
                'isFavorite': bool(row['is_favorite']),
                'isDisliked': is_disliked,
                'uploadDate': row['created_at']
            })
        except Exception as e:
            logger.error(f"Error processing item {row['id']}: {e}")
            continue
    
    return items

def get_wardrobe_item(item_id):
    """Get a single wardrobe item by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure is_disliked column exists
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'is_disliked' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN is_disliked INTEGER DEFAULT 0')
        conn.commit()
    
    cursor.execute('SELECT * FROM wardrobe_items WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # Check if is_disliked column exists
    is_disliked = False
    if 'is_disliked' in row.keys():
        is_disliked = bool(row['is_disliked'])
    
    # Safely get color fields
    color_rgb = None
    if 'color_rgb' in row.keys() and row['color_rgb']:
        try:
            color_rgb = json.loads(row['color_rgb'])
        except:
            pass
    
    all_colors = []
    if 'all_colors' in row.keys() and row['all_colors']:
        try:
            all_colors = json.loads(row['all_colors'])
        except:
            pass
    
    return {
        'id': row['id'],
        'filename': row['filename'],
        'primaryColor': row['primary_color'] if 'primary_color' in row.keys() else None,
        'colorRgb': color_rgb,
        'allColors': all_colors,
        'url': row['image_path'],
        'type': row['clothing_type'],
        'confidence': row['confidence'],
        'top5': json.loads(row['top_5']) if row['top_5'] else [],
        'eventScores': json.loads(row['event_scores']) if row['event_scores'] else {},
        'bestEvent': row['best_event'],
        'wearCount': row['wear_count'],
        'lastWorn': row['last_worn'],
        'wearHistory': json.loads(row['wear_history']) if row['wear_history'] else [],
        'isFavorite': bool(row['is_favorite']),
        'isDisliked': is_disliked,
        'uploadDate': row['created_at']
    }

def update_item_type(item_id, new_type, event_scores):
    """Update clothing type, event scores, and best event"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate best event from scores
    best_event = max(event_scores, key=event_scores.get) if event_scores else "Casual"
    
    cursor.execute('''
        UPDATE wardrobe_items 
        SET clothing_type = ?, event_scores = ?, best_event = ?
        WHERE id = ?
    ''', (new_type, json.dumps(event_scores), best_event, item_id))
    
    conn.commit()
    conn.close()
    logger.info(f"✅ Updated item {item_id}: type={new_type}, best_event={best_event}")

def toggle_favorite(item_id):
    """Toggle favorite status"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT is_favorite FROM wardrobe_items WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    
    if row:
        new_status = 0 if row['is_favorite'] else 1
        cursor.execute('UPDATE wardrobe_items SET is_favorite = ? WHERE id = ?', (new_status, item_id))
        conn.commit()
        conn.close()
        return bool(new_status)
    
    conn.close()
    return False

def toggle_dislike(item_id):
    """Toggle dislike status"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # First ensure the is_disliked column exists
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'is_disliked' not in columns:
        cursor.execute('ALTER TABLE wardrobe_items ADD COLUMN is_disliked INTEGER DEFAULT 0')
        conn.commit()
    
    cursor.execute('SELECT is_disliked FROM wardrobe_items WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    
    if row:
        # Safely get the value with fallback
        current_status = 0
        if 'is_disliked' in row.keys():
            current_status = row['is_disliked'] or 0
        new_status = 0 if current_status else 1
        cursor.execute('UPDATE wardrobe_items SET is_disliked = ? WHERE id = ?', (new_status, item_id))
        conn.commit()
        conn.close()
        return bool(new_status)
    
    conn.close()
    return False

def mark_item_worn(item_id, occasion, date=None):
    """Mark item as worn"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if date is None:
        date = datetime.now().isoformat()
    
    # Get current wear history
    cursor.execute('SELECT wear_history, wear_count FROM wardrobe_items WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    
    if row:
        wear_history = json.loads(row['wear_history']) if row['wear_history'] else []
        wear_history.append({'date': date, 'occasion': occasion})
        
        cursor.execute('''
            UPDATE wardrobe_items 
            SET wear_count = ?, last_worn = ?, wear_history = ?
            WHERE id = ?
        ''', (row['wear_count'] + 1, date, json.dumps(wear_history), item_id))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Marked item {item_id} as worn")
        return True
    
    conn.close()
    return False

def delete_item(item_id):
    """Delete a wardrobe item"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM wardrobe_items WHERE id = ?', (item_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    if deleted:
        logger.info(f"✅ Deleted item {item_id}")
    
    return deleted

def get_user_profile():
    """Get user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM user_profile WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'stylePreferences': json.loads(row['style_preferences']) if row['style_preferences'] else {},
            'totalInteractions': row['total_interactions'],
            'updatedAt': row['updated_at']
        }
    
    return None

def update_user_profile(style_preferences=None, increment_interactions=False):
    """Update user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if style_preferences:
        cursor.execute('''
            UPDATE user_profile 
            SET style_preferences = ?, updated_at = ?
            WHERE id = 1
        ''', (json.dumps(style_preferences), datetime.now().isoformat()))
    
    if increment_interactions:
        cursor.execute('''
            UPDATE user_profile 
            SET total_interactions = total_interactions + 1, updated_at = ?
            WHERE id = 1
        ''', (datetime.now().isoformat(),))
    
    conn.commit()
    conn.close()
    logger.info("✅ Updated user profile")

def get_analytics():
    """Get wardrobe analytics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Basic stats
    cursor.execute('SELECT COUNT(*) as total FROM wardrobe_items')
    total_items = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as unworn FROM wardrobe_items WHERE wear_count = 0')
    unworn_items = cursor.fetchone()['unworn']
    
    cursor.execute('SELECT AVG(wear_count) as avg_wear FROM wardrobe_items')
    avg_wear = cursor.fetchone()['avg_wear'] or 0
    
    cursor.execute('SELECT COUNT(*) as favorites FROM wardrobe_items WHERE is_favorite = 1')
    favorite_count = cursor.fetchone()['favorites']
    
    # Composition by clothing type
    cursor.execute('''
        SELECT clothing_type, COUNT(*) as count 
        FROM wardrobe_items 
        GROUP BY clothing_type
    ''')
    composition = cursor.fetchall()
    
    conn.close()
    
    return {
        'totalItems': total_items,
        'unwornItems': unworn_items,
        'avgWearCount': round(avg_wear, 1),
        'favoriteCount': favorite_count,
        'composition': [{'name': row['clothing_type'], 'value': row['count']} for row in composition]
    }

def get_matching_items(item_id, matching_types, matching_colors):
    """
    Find wardrobe items that match with the given item based on type and color
    
    Args:
        item_id: ID of the item to find matches for
        matching_types: List of clothing types that pair well
        matching_colors: List of colors that match
    
    Returns:
        List of matching wardrobe items
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure color columns exist
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'primary_color' not in columns:
        conn.close()
        return []
    
    # Build query to find matching items
    # Match by clothing type OR by color (flexible matching)
    placeholders_types = ','.join(['?'] * len(matching_types))
    placeholders_colors = ','.join(['?'] * len(matching_colors))
    
    query = f'''
        SELECT * FROM wardrobe_items 
        WHERE id != ? 
        AND (
            clothing_type IN ({placeholders_types})
            OR primary_color IN ({placeholders_colors})
        )
        ORDER BY 
            CASE WHEN clothing_type IN ({placeholders_types}) THEN 1 ELSE 2 END,
            wear_count DESC
        LIMIT 20
    '''
    
    params = [item_id] + matching_types + matching_colors + matching_types
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    matches = []
    for row in rows:
        try:
            # Check if is_disliked column exists
            is_disliked = False
            if 'is_disliked' in row.keys():
                is_disliked = bool(row['is_disliked'])
            
            match_reason = []
            if row['clothing_type'] in matching_types:
                match_reason.append(f"Type: {row['clothing_type']}")
            if row['primary_color'] and row['primary_color'] in matching_colors:
                match_reason.append(f"Color: {row['primary_color']}")
            
            # Safely get color RGB
            color_rgb = None
            if 'color_rgb' in row.keys() and row['color_rgb']:
                try:
                    color_rgb = json.loads(row['color_rgb'])
                except:
                    pass
            
            matches.append({
                'id': row['id'],
                'filename': row['filename'],
                'url': row['image_path'],
                'type': row['clothing_type'],
                'confidence': row['confidence'],
                'primaryColor': row['primary_color'] if 'primary_color' in row.keys() else None,
                'colorRgb': color_rgb,
                'bestEvent': row['best_event'],
                'wearCount': row['wear_count'],
                'isFavorite': bool(row['is_favorite']),
                'isDisliked': is_disliked,
                'matchReason': ' | '.join(match_reason),
                'uploadDate': row['created_at']
            })
        except Exception as e:
            logger.error(f"Error processing matching item {row['id']}: {e}")
            continue
    
    return matches

def update_item_purchase_info(item_id, purchase_price=None, purchase_date=None, season=None):
    """Update purchase information for an item"""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if purchase_price is not None:
        updates.append('purchase_price = ?')
        params.append(purchase_price)
    
    if purchase_date is not None:
        updates.append('purchase_date = ?')
        params.append(purchase_date)
    
    if season is not None:
        updates.append('season = ?')
        params.append(season)
    
    if updates:
        query = f"UPDATE wardrobe_items SET {', '.join(updates)} WHERE id = ?"
        params.append(item_id)
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        logger.info(f"✅ Updated purchase info for item {item_id}")
        return True
    
    conn.close()
    return False

def get_items_by_season(season):
    """Get items for a specific season"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM wardrobe_items WHERE season = ?', (season,))
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for row in rows:
        items.append({
            'id': row['id'],
            'filename': row['filename'],
            'url': row['image_path'],
            'type': row['clothing_type'],
            'season': row['season'],
            'wearCount': row['wear_count'],
            'lastWorn': row['last_worn']
        })
    
    return items

def get_unworn_items_since(days):
    """Get items not worn for specified days"""
    conn = get_connection()
    cursor = conn.cursor()
    
    from datetime import datetime, timedelta
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    cursor.execute('''
        SELECT * FROM wardrobe_items 
        WHERE last_worn IS NULL OR last_worn < ?
        ORDER BY wear_count ASC
    ''', (cutoff_date,))
    
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for row in rows:
        items.append({
            'id': row['id'],
            'filename': row['filename'],
            'url': row['image_path'],
            'type': row['clothing_type'],
            'wearCount': row['wear_count'],
            'lastWorn': row['last_worn'],
            'daysSinceWorn': None if not row['last_worn'] else (datetime.now() - datetime.fromisoformat(row['last_worn'])).days
        })
    
    return items

# Initialize database on module import
init_database()
