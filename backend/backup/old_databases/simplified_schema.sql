-- SIMPLIFIED 4-TABLE DATABASE SCHEMA
-- Easier to understand and manage

-- ============================================================================
-- TABLE 1: BRANDS
-- Purpose: Store information about clothing brands
-- ============================================================================
CREATE TABLE IF NOT EXISTS brands (
    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    brand_country VARCHAR(50),
    size_system VARCHAR(20),
    website_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLE 2: GARMENT CATEGORIES  
-- Purpose: Define types of garments (shirts, jeans, dresses, etc.)
-- ============================================================================
CREATE TABLE IF NOT EXISTS garment_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_name, gender)
);

-- ============================================================================
-- TABLE 3: SIZE CHARTS
-- Purpose: Link brands with garment categories (creates the size chart)
-- This is the BRIDGE TABLE that connects brands to categories
-- ============================================================================
CREATE TABLE IF NOT EXISTS size_charts (
    chart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    chart_name VARCHAR(100),
    fit_type VARCHAR(30) DEFAULT 'Regular',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES garment_categories(category_id) ON DELETE CASCADE,
    UNIQUE(brand_id, category_id, fit_type)
);

-- ============================================================================
-- TABLE 4: SIZES
-- Purpose: Store size labels AND all measurements in one place
-- This combines what used to be two separate tables (sizes + measurements)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_id INTEGER NOT NULL,
    size_label VARCHAR(20) NOT NULL,
    size_order INTEGER NOT NULL,
    
    -- Chest measurements (for tops, shirts, jackets, dresses)
    chest_min REAL,
    chest_max REAL,
    
    -- Shoulder measurements (for tops, shirts, jackets)
    shoulder_min REAL,
    shoulder_max REAL,
    
    -- Waist measurements (for all garments)
    waist_min REAL,
    waist_max REAL,
    
    -- Hip measurements (for pants, jeans, dresses)
    hip_min REAL,
    hip_max REAL,
    
    -- Arm length (for shirts, jackets with sleeves)
    arm_length_min REAL,
    arm_length_max REAL,
    
    -- Leg length (for pants, jeans)
    leg_length_min REAL,
    leg_length_max REAL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chart_id) REFERENCES size_charts(chart_id) ON DELETE CASCADE,
    UNIQUE(chart_id, size_label)
);

-- ============================================================================
-- OPTIONAL: USER MEASUREMENTS TABLE
-- Store user body measurements for quick reference
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_measurements (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_identifier VARCHAR(255),
    height REAL,
    chest REAL,
    waist REAL,
    hip REAL,
    shoulder_breadth REAL,
    shoulder_to_crotch REAL,
    arm_length REAL,
    leg_length REAL,
    gender VARCHAR(20),
    unit VARCHAR(10) DEFAULT 'cm',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_size_charts_brand ON size_charts(brand_id);
CREATE INDEX IF NOT EXISTS idx_size_charts_category ON size_charts(category_id);
CREATE INDEX IF NOT EXISTS idx_sizes_chart ON sizes(chart_id);

-- ============================================================================
-- SUMMARY
-- ============================================================================
-- 4 main tables:
-- 1. brands          - Who makes the clothes
-- 2. garment_categories - What type of clothing
-- 3. size_charts     - Links brand + category (the bridge)
-- 4. sizes           - Size labels + all measurements together
--
-- Additional optional table:
-- 5. user_measurements - Store user body data
-- ============================================================================
