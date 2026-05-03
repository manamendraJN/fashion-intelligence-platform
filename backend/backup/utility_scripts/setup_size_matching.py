"""
Quick Setup Script for Size Matching System
Automates database initialization and verification
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import db_manager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run complete setup"""
    
    print("\n" + "="*70)
    print("🚀 Fashion Intelligence Platform - Size Matching System Setup")
    print("="*70 + "\n")
    
    # Step 1: Check if database exists
    db_path = Path(__file__).parent.parent / "database" / "fashion_db.sqlite"
    
    if db_path.exists():
        logger.warning(f"⚠️  Database already exists at {db_path}")
        response = input("Do you want to reinitialize? This will DELETE all data. (yes/no): ")
        
        if response.lower() != 'yes':
            logger.info("Setup cancelled. Using existing database.")
            verify_database()
            return
        else:
            db_path.unlink()
            logger.info("🗑️  Existing database deleted")
    
    # Step 2: Initialize database
    logger.info("📦 Creating database schema...")
    try:
        db_manager.initialize_database()
        logger.info("✅ Database schema created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating schema: {e}")
        return
    
    # Step 3: Populate with sample data
    logger.info("📊 Populating sample data...")
    try:
        from database.populate_sample_data import populate_sample_data
        populate_sample_data()
        logger.info("✅ Sample data loaded successfully")
    except Exception as e:
        logger.error(f"❌ Error loading sample data: {e}")
        return
    
    # Step 4: Verify setup
    logger.info("\n" + "="*70)
    logger.info("🔍 Verifying Setup...")
    logger.info("="*70)
    
    verify_database()
    
    # Step 5: Show next steps
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Next Steps:\n")
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python app.py")
    print()
    print("2. Test the API:")
    print("   curl http://localhost:5000/api/size/health")
    print()
    print("3. Get a size recommendation:")
    print('   curl -X POST http://localhost:5000/api/size/recommend \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"measurements": {"chest": 95, "waist": 82}, "brand_id": 1, "category_id": 1}\'')
    print()
    print("4. Read the documentation:")
    print("   - docs/SETUP_AND_USAGE_GUIDE.md")
    print("   - docs/SIZE_MATCHING_SYSTEM.md")
    print()
    print("="*70 + "\n")


def verify_database():
    """Verify database contents"""
    try:
        # Check brands
        brands = db_manager.get_brands()
        logger.info(f"✅ Brands: {len(brands)} loaded")
        for brand in brands:
            logger.info(f"   - {brand['brand_name']} ({brand['size_system']})")
        
        # Check categories
        categories = db_manager.get_categories()
        logger.info(f"✅ Categories: {len(categories)} loaded")
        for cat in categories[:5]:  # Show first 5
            logger.info(f"   - {cat['category_name']} ({cat['gender']})")
        if len(categories) > 5:
            logger.info(f"   ... and {len(categories) - 5} more")
        
        # Test a recommendation
        logger.info("✅ Testing recommendation engine...")
        from services.size_matching_service import size_matching_service
        
        test_measurements = {
            'chest': 95,
            'shoulder_breadth': 45,
            'waist': 82
        }
        
        result = size_matching_service.find_best_size(
            test_measurements,
            brand_id=1,
            category_id=1
        )
        
        if 'error' not in result:
            logger.info(f"   ✓ Test successful: Size {result['recommended_size']} "
                       f"with {result['confidence']:.1f}% confidence")
        else:
            logger.warning(f"   ⚠️ Test failed: {result['error']}")
        
    except Exception as e:
        logger.error(f"❌ Verification error: {e}")


def run_quick_test():
    """Run a quick test of the system"""
    print("\n" + "="*70)
    print("🧪 Running Quick Test")
    print("="*70 + "\n")
    
    from services.size_matching_service import size_matching_service
    
    test_cases = [
        {
            'name': 'Athletic Male',
            'measurements': {'chest': 102, 'shoulder_breadth': 48, 'waist': 85},
            'brand_id': 1,
            'category_id': 1
        },
        {
            'name': 'Average Female',
            'measurements': {'chest': 88, 'waist': 68, 'hip': 94},
            'brand_id': 3,
            'category_id': 7
        }
    ]
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Measurements: {test['measurements']}")
        
        result = size_matching_service.find_best_size(
            test['measurements'],
            test['brand_id'],
            test['category_id']
        )
        
        if 'error' not in result:
            print(f"✅ Recommended Size: {result['recommended_size']}")
            print(f"   Confidence: {result['confidence']:.1f}%")
            print(f"   Brand: {result['brand_name']}")
        else:
            print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Size Matching System')
    parser.add_argument('--test', action='store_true', help='Run quick test after setup')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing database')
    
    args = parser.parse_args()
    
    if args.verify_only:
        print("\n🔍 Verifying existing database...\n")
        verify_database()
    else:
        main()
        
        if args.test:
            run_quick_test()
