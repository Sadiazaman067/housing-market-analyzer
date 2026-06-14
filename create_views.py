import sqlite3

conn = sqlite3.connect("housing.db")
cursor = conn.cursor()

# View 1: Average sale price by neighborhood
cursor.executescript("""
    DROP VIEW IF EXISTS neighborhood_stats;
    CREATE VIEW neighborhood_stats AS
    SELECT 
        n.NeighborhoodName,
        ROUND(AVG(s.SalePrice), 2) AS avg_price,
        ROUND(MIN(s.SalePrice), 2) AS min_price,
        ROUND(MAX(s.SalePrice), 2) AS max_price,
        COUNT(*) AS num_sales
    FROM Sales s
    JOIN Properties p ON s.PID = p.PID
    JOIN Neighborhoods n ON p.NeighborhoodID = n.NeighborhoodID
    GROUP BY n.NeighborhoodName
    ORDER BY avg_price DESC;
""")

# View 2: Price per square foot by neighborhood
cursor.executescript("""
    DROP VIEW IF EXISTS price_per_sqft;
    CREATE VIEW price_per_sqft AS
    SELECT 
        n.NeighborhoodName,
        ROUND(AVG(CAST(s.SalePrice AS FLOAT) / p.GrLivArea), 2) AS avg_price_per_sqft
    FROM Sales s
    JOIN Properties p ON s.PID = p.PID
    JOIN Neighborhoods n ON p.NeighborhoodID = n.NeighborhoodID
    WHERE p.GrLivArea > 0
    GROUP BY n.NeighborhoodName
    ORDER BY avg_price_per_sqft DESC;
""")

# View 3: Year over year sales trends
cursor.executescript("""
    DROP VIEW IF EXISTS yearly_trends;
    CREATE VIEW yearly_trends AS
    SELECT 
        YrSold,
        COUNT(*) AS total_sales,
        ROUND(AVG(SalePrice), 2) AS avg_price,
        ROUND(MIN(SalePrice), 2) AS min_price,
        ROUND(MAX(SalePrice), 2) AS max_price
    FROM Sales
    GROUP BY YrSold
    ORDER BY YrSold;
""")

# View 4: Outlier detection — properties priced 2 std devs above neighborhood average
cursor.executescript("""
    DROP VIEW IF EXISTS outlier_properties;
    CREATE VIEW outlier_properties AS
    SELECT 
        s.PID,
        n.NeighborhoodName,
        s.SalePrice,
        ns.avg_price,
        ROUND(s.SalePrice - ns.avg_price, 2) AS price_diff
    FROM Sales s
    JOIN Properties p ON s.PID = p.PID
    JOIN Neighborhoods n ON p.NeighborhoodID = n.NeighborhoodID
    JOIN neighborhood_stats ns ON n.NeighborhoodName = ns.NeighborhoodName
    WHERE s.SalePrice > ns.avg_price * 1.5
    ORDER BY price_diff DESC;
""")

conn.commit()
conn.close()

print("Views created successfully:")
print("  - neighborhood_stats")
print("  - price_per_sqft")
print("  - yearly_trends")
print("  - outlier_properties")