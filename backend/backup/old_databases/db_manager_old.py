"""
Database Manager for Fashion Intelligence Platform
Handles SQLite database initialization, connections, and basic operations
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file. Defaults to backend/database/fashion_db.sqlite
        """
        if db_path is None:
            db_path = Path(__file__).parent / "fashion_db.sqlite"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Database initialized at: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def initialize_database(self):
        """Create database schema from SQL file"""
        schema_path = Path(__file__).parent / "schema.sql"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            logger.info("✅ Database schema initialized successfully")
    
    def get_or_create_brand(self, name: str, country: str = None, 
                            size_system: str = None, website: str = None, 
                            notes: str = None) -> int:
        """Get existing brand or create new one, return brand_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Check if brand exists
            cursor.execute("""
                SELECT brand_id FROM brands WHERE brand_name = ?
            """, (name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            # Create new brand
            cursor.execute("""
                INSERT INTO brands (brand_name, brand_country, size_system, website_url, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, country, size_system, website, notes))
            return cursor.lastrowid
    
    def insert_brand(self, name: str, country: str = None, 
                     size_system: str = None, website: str = None, 
                     notes: str = None) -> int:
        """Insert a new brand and return brand_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO brands (brand_name, brand_country, size_system, website_url, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, country, size_system, website, notes))
            return cursor.lastrowid
    
    def get_or_create_category(self, name: str, gender: str, description: str = None) -> int:
        """Get existing category or create new one, return category_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Check if category exists
            cursor.execute("""
                SELECT category_id FROM garment_categories 
                WHERE category_name = ? AND gender = ?
            """, (name, gender))
            result = cursor.fetchone()
            if result:
                return result[0]
            # Create new category
            cursor.execute("""
                INSERT INTO garment_categories (category_name, gender, description)
                VALUES (?, ?, ?)
            """, (name, gender, description))
            return cursor.lastrowid
    
    def insert_category(self, name: str, gender: str, description: str = None) -> int:
        """Insert a new garment category and return category_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO garment_categories (category_name, gender, description)
                VALUES (?, ?, ?)
            """, (name, gender, description))
            return cursor.lastrowid
    
    def insert_size_chart(self, brand_id: int, category_id: int, 
                          chart_name: str = None, fit_type: str = 'Regular',
                          notes: str = None) -> int:
        """Insert a new size chart and return chart_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO size_charts (brand_id, category_id, chart_name, fit_type, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (brand_id, category_id, chart_name, fit_type, notes))
            return cursor.lastrowid
    
    def insert_size(self, chart_id: int, size_label: str, size_order: int) -> int:
        """Insert a size and return size_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sizes (chart_id, size_label, size_order)
                VALUES (?, ?, ?)
            """, (chart_id, size_label, size_order))
            return cursor.lastrowid
    
    def insert_size_measurement(self, size_id: int, measurement_type: str,
                                min_val: float = None, max_val: float = None,
                                optimal_val: float = None, tolerance: float = 2.0,
                                weight: float = 1.0):
        """Insert measurement ranges for a specific size"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO size_measurements 
                (size_id, measurement_type, min_value, max_value, optimal_value, tolerance, weight)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (size_id, measurement_type, min_val, max_val, optimal_val, tolerance, weight))
    
    def insert_category_measurement_mapping(self, category_id: int, 
                                           measurement_type: str,
                                           importance_weight: float = 1.0,
                                           is_required: bool = True,
                                           description: str = None):
        """Map which measurements are important for a garment category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO category_measurements 
                (category_id, measurement_type, importance_weight, is_required, description)
                VALUES (?, ?, ?, ?, ?)
            """, (category_id, measurement_type, importance_weight, is_required, description))
    
    def get_brands(self) -> List[Dict]:
        """Get all brands"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM brands ORDER BY brand_name")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_categories(self, gender: str = None) -> List[Dict]:
        """Get garment categories, optionally filtered by gender"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if gender:
                cursor.execute(
                    "SELECT * FROM garment_categories WHERE gender = ? OR gender = 'Unisex' ORDER BY category_name",
                    (gender,)
                )
            else:
                cursor.execute("SELECT * FROM garment_categories ORDER BY category_name")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_size_chart(self, brand_id: int, category_id: int, 
                       fit_type: str = 'Regular') -> Optional[Dict]:
        """Get size chart details for a specific brand and category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sc.*, b.brand_name, b.size_system, gc.category_name, gc.gender
                FROM size_charts sc
                JOIN brands b ON sc.brand_id = b.brand_id
                JOIN garment_categories gc ON sc.category_id = gc.category_id
                WHERE sc.brand_id = ? AND sc.category_id = ? AND sc.fit_type = ? AND sc.is_active = 1
            """, (brand_id, category_id, fit_type))
            
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_sizes_for_chart(self, chart_id: int) -> List[Dict]:
        """Get all sizes for a specific chart with their measurements"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.size_id, s.size_label, s.size_order,
                       sm.measurement_type, sm.min_value, sm.max_value, 
                       sm.optimal_value, sm.tolerance, sm.weight
                FROM sizes s
                LEFT JOIN size_measurements sm ON s.size_id = sm.size_id
                WHERE s.chart_id = ?
                ORDER BY s.size_order, sm.measurement_type
            """, (chart_id,))
            
            # Group measurements by size
            sizes = {}
            for row in cursor.fetchall():
                row_dict = dict(row)
                size_id = row_dict['size_id']
                
                if size_id not in sizes:
                    sizes[size_id] = {
                        'size_id': size_id,
                        'size_label': row_dict['size_label'],
                        'size_order': row_dict['size_order'],
                        'measurements': []
                    }
                
                if row_dict['measurement_type']:
                    sizes[size_id]['measurements'].append({
                        'type': row_dict['measurement_type'],
                        'min': row_dict['min_value'],
                        'max': row_dict['max_value'],
                        'optimal': row_dict['optimal_value'],
                        'tolerance': row_dict['tolerance'],
                        'weight': row_dict['weight']
                    })
            
            return list(sizes.values())
    
    def get_category_measurement_requirements(self, category_id: int) -> List[Dict]:
        """Get required measurements for a garment category"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT measurement_type, importance_weight, is_required, description
                FROM category_measurements
                WHERE category_id = ?
                ORDER BY importance_weight DESC
            """, (category_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def save_user_measurements(self, measurements: Dict[str, float], 
                              user_identifier: str = None,
                              gender: str = None,
                              measured_at: str = None) -> int:
        """Save user body measurements with optional timestamp"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if measured_at:
                # If timestamp provided, use it (convert ISO to SQLite format)
                from datetime import datetime
                dt = datetime.fromisoformat(measured_at.replace('Z', '+00:00'))
                timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute("""
                    INSERT INTO user_measurements 
                    (user_identifier, height, chest, waist, hip, shoulder_breadth, 
                     shoulder_to_crotch, arm_length, bicep, forearm, wrist, 
                     leg_length, thigh, calf, ankle, gender, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_identifier,
                    measurements.get('height'),
                    measurements.get('chest'),
                    measurements.get('waist'),
                    measurements.get('hip'),
                    measurements.get('shoulder_breadth'),
                    measurements.get('shoulder_to_crotch'),
                    measurements.get('arm_length'),
                    measurements.get('bicep'),
                    measurements.get('forearm'),
                    measurements.get('wrist'),
                    measurements.get('leg_length'),
                    measurements.get('thigh'),
                    measurements.get('calf'),
                    measurements.get('ankle'),
                    gender,
                    timestamp_str
                ))
            else:
                # Use default CURRENT_TIMESTAMP
                cursor.execute("""
                    INSERT INTO user_measurements 
                    (user_identifier, height, chest, waist, hip, shoulder_breadth, 
                     shoulder_to_crotch, arm_length, bicep, forearm, wrist, 
                     leg_length, thigh, calf, ankle, gender)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_identifier,
                    measurements.get('height'),
                    measurements.get('chest'),
                    measurements.get('waist'),
                    measurements.get('hip'),
                    measurements.get('shoulder_breadth'),
                    measurements.get('shoulder_to_crotch'),
                    measurements.get('arm_length'),
                    measurements.get('bicep'),
                    measurements.get('forearm'),
                    measurements.get('wrist'),
                    measurements.get('leg_length'),
                    measurements.get('thigh'),
                    measurements.get('calf'),
                    measurements.get('ankle'),
                    gender
                ))
            return cursor.lastrowid
    
    def get_latest_user_measurements(self, user_identifier: str = 'default', 
                                     max_age_days: int = 90) -> Optional[Dict]:
        """
        Get most recent user measurements within specified age
        
        Args:
            user_identifier: User identifier (default: 'default' for anonymous users)
            max_age_days: Maximum age of measurements in days (default: 90 days / 3 months)
        
        Returns:
            Dictionary with measurements and metadata, or None if no recent measurements found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_measurements
                WHERE user_identifier = ? 
                AND datetime(created_at) >= datetime('now', '-' || ? || ' days')
                ORDER BY created_at DESC
                LIMIT 1
            """, (user_identifier, max_age_days))
            
            result = cursor.fetchone()
            if result:
                data = dict(result)
                # Extract measurements into a separate dict
                measurements = {
                    'height': data.get('height'),
                    'chest': data.get('chest'),
                    'waist': data.get('waist'),
                    'hip': data.get('hip'),
                    'shoulder_breadth': data.get('shoulder_breadth'),
                    'shoulder_to_crotch': data.get('shoulder_to_crotch'),
                    'arm_length': data.get('arm_length'),
                    'bicep': data.get('bicep'),
                    'forearm': data.get('forearm'),
                    'wrist': data.get('wrist'),
                    'leg_length': data.get('leg_length'),
                    'thigh': data.get('thigh'),
                    'calf': data.get('calf'),
                    'ankle': data.get('ankle')
                }
                # Remove None values
                measurements = {k: v for k, v in measurements.items() if v is not None}
                
                return {
                    'user_id': data['user_id'],
                    'measurements': measurements,
                    'gender': data.get('gender'),
                    'unit': data.get('unit', 'cm'),
                    'measured_at': data['created_at'],
                    'age_days': None  # Can be calculated on frontend
                }
            return None
    
    def get_all_user_measurements(self, user_identifier: str = 'default') -> List[Dict]:
        """Get all measurements for a user, ordered by most recent first"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_measurements
                WHERE user_identifier = ?
                ORDER BY created_at DESC
            """, (user_identifier,))
            return [dict(row) for row in cursor.fetchall()]
    
    def log_recommendation(self, user_id: int, brand_id: int, 
                          category_id: int, recommended_size: str,
                          confidence_score: float, match_details: Dict):
        """Log a size recommendation for analytics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO recommendation_log 
                (user_id, brand_id, category_id, recommended_size, confidence_score, match_details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, brand_id, category_id, recommended_size, 
                  confidence_score, json.dumps(match_details)))
    
    def clear_all_data(self):
        """Clear all data from database (for testing)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            tables = ['recommendation_log', 'user_measurements', 'size_measurements',
                     'sizes', 'size_charts', 'category_measurements', 
                     'garment_categories', 'brands']
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
            logger.warning("⚠️  All data cleared from database")


# Singleton instance
db_manager = DatabaseManager()
