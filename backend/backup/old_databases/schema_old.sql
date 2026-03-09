-- Fashion Intelligence Platform - Size Matching Database Schema
-- Purpose: Store brand-specific garment size charts and measurement mappings

-- ============================================================================
-- BRANDS TABLE
-- Stores information about clothing brands
-- ============================================================================
CREATE TABLE IF NOT EXISTS brands (
    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    brand_country VARCHAR(50),  -- e.g., 'USA', 'UK', 'EU', 'Asia'
    size_system VARCHAR(20),     -- e.g., 'US', 'UK', 'EU', 'International'
    website_url VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- GARMENT CATEGORIES TABLE
-- Defines types of garments (e.g., shirts, pants, dresses)
-- ============================================================================
CREATE TABLE IF NOT EXISTS garment_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL,  -- e.g., 'Shirt', 'Pants', 'Dress', 'Jacket'
    gender VARCHAR(20) NOT NULL,                 -- 'Men', 'Women', 'Unisex'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_name, gender)  -- Composite unique constraint
);

-- ============================================================================
-- SIZE CHARTS TABLE
-- Links brands to their specific size charts for different garment categories
-- ============================================================================
CREATE TABLE IF NOT EXISTS size_charts (
    chart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    chart_name VARCHAR(100),  -- e.g., "Nike Men's Athletic Shirts"
    fit_type VARCHAR(30),     -- e.g., 'Regular', 'Slim', 'Relaxed', 'Athletic'
    notes TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES garment_categories(category_id) ON DELETE CASCADE,
    UNIQUE(brand_id, category_id, fit_type)
);

-- ============================================================================
-- SIZES TABLE
-- Defines the size labels (XS, S, M, L, XL, numeric, etc.) for each size chart
-- ============================================================================
CREATE TABLE IF NOT EXISTS sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_id INTEGER NOT NULL,
    size_label VARCHAR(20) NOT NULL,  -- e.g., 'S', 'M', 'L', '32', '34', '6', '8'
    size_order INTEGER NOT NULL,      -- Numeric order for sorting (1=smallest, increasing)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chart_id) REFERENCES size_charts(chart_id) ON DELETE CASCADE,
    UNIQUE(chart_id, size_label)
);

-- ============================================================================
-- SIZE MEASUREMENTS TABLE
-- Stores the actual body measurement ranges for each size
-- Maps which body measurements are relevant for each garment type
-- ============================================================================
CREATE TABLE IF NOT EXISTS size_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_id INTEGER NOT NULL,
    measurement_type VARCHAR(50) NOT NULL,  -- 'chest', 'waist', 'hip', 'shoulder_breadth', etc.
    min_value REAL,           -- Minimum measurement in cm
    max_value REAL,           -- Maximum measurement in cm
    optimal_value REAL,       -- Ideal/target measurement in cm (optional)
    tolerance REAL DEFAULT 2.0, -- Acceptable deviation in cm (for matching algorithm)
    weight REAL DEFAULT 1.0,  -- Importance weight for this measurement (0.0-1.0)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (size_id) REFERENCES sizes(size_id) ON DELETE CASCADE,
    UNIQUE(size_id, measurement_type)
);

-- ============================================================================
-- MEASUREMENT MAPPING TABLE
-- Maps which body measurements are important for each garment category
-- ============================================================================
CREATE TABLE IF NOT EXISTS category_measurements (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    measurement_type VARCHAR(50) NOT NULL,  -- 'chest', 'waist', 'hip', etc.
    importance_weight REAL DEFAULT 1.0,     -- How critical this measurement is (0.0-1.0)
    is_required BOOLEAN DEFAULT 1,          -- Must be present for matching
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES garment_categories(category_id) ON DELETE CASCADE,
    UNIQUE(category_id, measurement_type)
);

-- ============================================================================
-- USER MEASUREMENTS TABLE (Optional - for saving user profiles)
-- Stores user body measurements for quick reference
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_measurements (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_identifier VARCHAR(255),  -- Email, username, or anonymous ID
    height REAL,
    chest REAL,
    waist REAL,
    hip REAL,
    shoulder_breadth REAL,
    shoulder_to_crotch REAL,
    arm_length REAL,
    bicep REAL,
    forearm REAL,
    wrist REAL,
    leg_length REAL,
    thigh REAL,
    calf REAL,
    ankle REAL,
    gender VARCHAR(20),
    unit VARCHAR(10) DEFAULT 'cm',  -- 'cm' or 'inches'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SIZE RECOMMENDATIONS LOG TABLE (Optional - for analytics)
-- Tracks size recommendations made by the system for analysis
-- ============================================================================
CREATE TABLE IF NOT EXISTS recommendation_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    brand_id INTEGER,
    category_id INTEGER,
    recommended_size VARCHAR(20),
    confidence_score REAL,
    match_details TEXT,  -- JSON with detailed matching scores
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_measurements(user_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES garment_categories(category_id)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_size_charts_brand ON size_charts(brand_id);
CREATE INDEX IF NOT EXISTS idx_size_charts_category ON size_charts(category_id);
CREATE INDEX IF NOT EXISTS idx_sizes_chart ON sizes(chart_id);
CREATE INDEX IF NOT EXISTS idx_size_measurements_size ON size_measurements(size_id);
CREATE INDEX IF NOT EXISTS idx_size_measurements_type ON size_measurements(measurement_type);
CREATE INDEX IF NOT EXISTS idx_category_measurements_category ON category_measurements(category_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_log_user ON recommendation_log(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_log_brand ON recommendation_log(brand_id);

-- ============================================================================
-- VIEWS FOR EASIER QUERYING
-- ============================================================================

-- Complete size chart view with all details
CREATE VIEW IF NOT EXISTS v_complete_size_chart AS
SELECT 
    sc.chart_id,
    b.brand_name,
    b.size_system,
    gc.category_name,
    gc.gender,
    sc.fit_type,
    s.size_label,
    s.size_order,
    sm.measurement_type,
    sm.min_value,
    sm.max_value,
    sm.optimal_value,
    sm.tolerance,
    sm.weight
FROM size_charts sc
JOIN brands b ON sc.brand_id = b.brand_id
JOIN garment_categories gc ON sc.category_id = gc.category_id
JOIN sizes s ON sc.chart_id = s.chart_id
LEFT JOIN size_measurements sm ON s.size_id = sm.size_id
WHERE sc. is_active = 1
ORDER BY b.brand_name, gc.category_name, s.size_order, sm.measurement_type;

-- Brand summary view
CREATE VIEW IF NOT EXISTS v_brand_summary AS
SELECT 
    b.brand_id,
    b.brand_name,
    b.size_system,
    COUNT(DISTINCT sc.chart_id) as total_charts,
    COUNT(DISTINCT gc.category_id) as total_categories,
    b.created_at
FROM brands b
LEFT JOIN size_charts sc ON b.brand_id = sc.brand_id
LEFT JOIN garment_categories gc ON sc.category_id = gc.category_id
GROUP BY b.brand_id;
