# E-Commerce SQL Analysis 📊

A comprehensive SQL data analysis project demonstrating advanced query techniques, database design, and actionable business intelligence insights using PostgreSQL and Python.

**Built to showcase:** Production-ready SQL skills, analytical thinking, and the ability to translate data into business recommendations.

---

## 🎯 Project Overview

This project analyzes e-commerce transaction data (50,000+ orders across 7 categories) to identify operational inefficiencies, revenue opportunities, and customer behavior patterns. The analysis uncovered critical issues including 20-30% return rates on best-selling products, ineffective discount strategies, and significant regional delivery gaps.

**Key Achievement:** Moved beyond descriptive analytics to provide actionable recommendations backed by data—quality alerts, margin optimization strategies, and customer conversion pathways.

---

## 💡 Executive Summary - Key Findings

### Critical Business Issues Identified

**🚨 Quality Crisis**
- 20-30% return rates on top-selling products (Fashion, Electronics, Sports)
- Sports category has worst performance despite strong margins
- Indicates systemic quality or product information issues

**💰 Margin Efficiency Paradox**
- Electronics: 45% of revenue, only 11% profit margin (volume trap)
- Sports/Fashion/Home/Beauty: 22%+ margins (high performers)
- Grocery: Low revenue AND low margin (no competitive advantage)

**📦 Operational Gaps**
- East region: 5+ day delivery average (unacceptable vs <3 day standard)
- North region: Fastest delivery despite highest volume (best practice exists)
- Discounts show minimal impact on quantity (only 0.03 unit difference across all tiers)

**👥 Customer Insights**
- 68% customer retention rate (repeat purchases)
- Top 20% of customers drive 60%+ of revenue
- Age group 26-35 has highest average order value ($89)
- Regional LTV varies significantly (North leads)

---

## 📊 Business Recommendations

### Immediate Actions

1. **Quality Investigation (High Priority)**
   - Root cause analysis on products with 20%+ return rates
   - Verify product descriptions match actual items
   - Implement quality gates before inventory approval

2. **Discount Strategy Overhaul**
   - Current discounts are margin-diluting without driving volume
   - Test targeted discounts on specific customer segments vs blanket promotions
   - Calculate break-even discount thresholds per category

3. **Delivery Optimization (East Region)**
   - Audit East region fulfillment process
   - Benchmark against North region best practices
   - Set service level targets: <3 days standard delivery

4. **Category Strategy**
   - Electronics = customer acquisition (accept low margin)
   - Actively convert Electronics buyers to high-margin categories (Fashion, Sports, Home)
   - Consider rationalizing Grocery (low revenue, low margin, no strategic value)

### Strategic Initiatives

5. **Customer Conversion Pathway**
   - Track Electronics → High-Margin category purchase sequences
   - Build product bundling (Electronics + Fashion/Sports)
   - Personalized post-purchase campaigns promoting complementary categories

6. **Payment Method ROI**
   - Credit/Debit dominate (80%+) across all regions uniformly
   - Evaluate costs of facilitating low-volume methods (UPI, COD, Wallet)
   - Potential cost savings by discontinuing unprofitable payment options

---

## 🗄️ Database Schema

**Architecture:** Star schema normalized to 3NF

### Entity Relationship Diagram
```
customers (1) ──→ (N) orders (1) ──→ (N) order_items (N) ──→ (1) products
```

### Tables

**Fact Table:**
- `order_items` - Transaction-level data (quantity, discount, total_amount, profit_margin, returned)

**Dimension Tables:**
- `customers` - 7,903 unique customers (customer_id, name, age, gender, region)
- `products` - 24,912 products (product_id, name, category, price)
- `orders` - Order metadata (order_id, customer_id, order_date, payment_method, shipping_cost, delivery_time_days)

**Design Rationale:**
- **3NF Normalization** - `customer_id` stored only in orders table (not order_items) to prevent update anomalies
- **Star Schema** - Optimized for analytical queries with fast joins
- **Separate Dimensions** - Enables flexible querying (e.g., customers without orders via LEFT JOIN)

---

## 📈 Analysis Framework - 17 Business Questions

### Revenue Analysis (5 queries)
1. **Top 10 products by revenue** → All Electronics (Smartwatch, Speaker, Phone categories)
2. **Monthly revenue trends with MoM growth** → 15%+ growth in peak periods, seasonal patterns identified
3. **Category revenue distribution** → Electronics 45%, Home 18%, Fashion 11%, Sports 11%
4. **Top 3 products per category** → Identified best performers across all 7 categories
5. **Cumulative revenue over time** → Running total showing growth trajectory

### Customer Insights (5 queries)
6. **Top 10 customers by lifetime value** → Range: $2,500-$4,200 per customer
7. **Customer retention rate** → 68% repeat purchase rate
8. **Average order value by age group** → 26-35 age bracket leads ($89 AOV)
9. **Regional customer LTV** → North region highest, Central lowest
10. **Gender purchasing patterns** → Male customers slightly higher AOV

### Product & Operations (5 queries)
11. **Products with highest return rates** → 20-30% on best-sellers (quality alert)
12. **Discount vs quantity correlation** → Minimal impact (0.03 unit difference)
13. **Delivery time by region** → East 5+ days (worst), North <3 days (best)
14. **Payment method preferences** → Credit/Debit 80%+ across all regions
15. **Category profit margins** → Sports/Fashion/Home 22%+, Electronics 11%, Grocery 10%

### Advanced Segmentation (2 queries)
16. **Inactive customers (LEFT JOIN)** → 127 customers with zero orders identified
17. **Customer spending quintiles (NTILE)** → Top 20% contribute 62% of revenue

---

## 🛠️ Technical Implementation

### SQL Techniques Demonstrated

**Window Functions:**
- `RANK()` - Top products per category
- `ROW_NUMBER()` - Customer purchase sequences
- `LAG()` - Month-over-month growth calculations
- `NTILE(5)` - Customer spending quintiles
- `SUM() OVER()` - Running totals, percentage of total calculations

**Advanced Queries:**
- **CTEs (WITH clauses)** - Monthly revenue aggregation, customer segmentation
- **Complex JOINs** - Multi-table joins (customers → orders → order_items → products)
- **LEFT JOIN** - Finding customers with zero orders
- **Subqueries** - Nested ranking queries for top-N per group
- **PARTITION BY** - Group-wise window calculations

**Aggregate & Date Functions:**
- `SUM()`, `AVG()`, `COUNT()`, `ROUND()`, `STDDEV()`
- `TO_CHAR()`, `DATE_TRUNC()` - Time-series aggregation
- **CASE statements** - Age bucketing, conditional aggregation
- **HAVING clause** - Multi-condition filtering on aggregates

**Database Design:**
- Foreign key constraints for referential integrity
- Composite primary keys (order_items)
- 3NF normalization to eliminate redundancy

---

## 🚀 Setup & Reproduction

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- 2GB disk space for database

### Quick Start

**1. Clone repository**
```bash
git clone https://github.com/JemHRice/ecommerce-sql-analysis
cd ecommerce-sql-analysis
```

**2. Set up environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**3. Configure database**

Create `.env` file:
```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
```

**4. Initialize database**
```bash
# Create database
psql -U postgres
CREATE DATABASE ecommerce;
\q

# Load data
python load_data.py

# Generate realistic names (optional)
python generate_names.py
```

**5. Run analysis**
```bash
jupyter notebook analysis.ipynb
```

---

## 📁 Project Structure

```
ecommerce-sql-analysis/
├── data/
│   └── ecommerce_data.csv          # Raw dataset (50k+ transactions)
├── schema.sql                       # Database DDL
├── load_data.py                     # Data loading script
├── generate_names.py                # Realistic name generation (Faker)
├── analysis.ipynb                   # Main analysis notebook
├── requirements.txt                 # Python dependencies
├── .env                             # Database credentials (not committed)
└── README.md
```

---

## 📊 Sample Analysis - Monthly Revenue with Growth

```sql
WITH monthly_revenue AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS month_year,
        SUM(total_amount) AS monthly_total
    FROM order_items
    JOIN orders USING (order_id)
    GROUP BY month_year
)
SELECT 
    month_year,
    monthly_total,
    LAG(monthly_total) OVER (ORDER BY month_year) AS prev_month,
    ROUND(
        ((monthly_total - LAG(monthly_total) OVER (ORDER BY month_year)) 
         / LAG(monthly_total) OVER (ORDER BY month_year) * 100), 
        2
    ) as mom_growth_pct
FROM monthly_revenue
ORDER BY month_year;
```

**Result:** Identified 15%+ growth periods and seasonal dips requiring inventory planning adjustments.

---

## 🎓 What This Project Demonstrates

### Technical Skills
- ✅ Writing production-quality SQL with window functions and CTEs
- ✅ Designing normalized database schemas (3NF)
- ✅ Python data analysis (Pandas, Matplotlib, SQLAlchemy)
- ✅ Database administration (PostgreSQL setup, data loading)
- ✅ Version control and documentation

### Analytical Skills
- ✅ Translating business questions into SQL queries
- ✅ Identifying root causes from data patterns (quality issues, operational gaps)
- ✅ Customer segmentation strategies (RFM, quintiles)
- ✅ Profitability analysis (margin vs volume trade-offs)
- ✅ Making data-driven recommendations with quantified impact

### Business Acumen
- ✅ Understanding margin dynamics (Electronics volume trap)
- ✅ Recognizing quality issues from return rate patterns
- ✅ Evaluating operational efficiency across regions
- ✅ Customer lifecycle thinking (acquisition → conversion → retention)

---

## 💼 Business Impact

**If this analysis were implemented:**

1. **Quality Improvement** - Reducing 25% return rate to industry standard 10% = $150k+ annual savings
2. **Margin Optimization** - Converting 20% of Electronics buyers to high-margin categories = 5-8% overall margin improvement
3. **Delivery Standardization** - East region matching North performance = improved NPS, reduced churn
4. **Discount Rationalization** - Eliminating ineffective promotions = 2-3% margin recovery

**Total Potential Annual Impact:** $200k-$500k for a mid-size e-commerce operation

---

## 🔮 Next Steps & Extensions

**Recommended Follow-Up Analyses:**

1. **Customer Journey Modeling**
   - First purchase category → subsequent purchases
   - Electronics-to-high-margin conversion rates
   - Time between purchases by segment

2. **Cohort Analysis**
   - Monthly cohorts tracked over 6-12 months
   - Retention curves by acquisition channel
   - LTV by first purchase category

3. **Price Elasticity**
   - Which products respond to discounts?
   - Optimal discount thresholds per category
   - Cannibalization effects

4. **Predictive Models**
   - Customer churn prediction (ML model)
   - Product return probability scoring
   - LTV forecasting

5. **A/B Testing Framework**
   - Bundling strategies (Electronics + high-margin items)
   - Regional marketing campaign effectiveness
   - Payment method incentive programs

---

## 🛠️ Technologies

| Component | Tool |
|-----------|------|
| Database | PostgreSQL 18.2 |
| Language | Python 3.13 |
| Analysis | Pandas, NumPy |
| Visualization | Matplotlib |
| Connector | SQLAlchemy, psycopg2 |
| Environment | Jupyter Notebook |
| Data Gen | Faker |

---

## 📜 Certifications & Learning

**SQL Skills Validated By:**
- DataCamp SQL Fundamentals Track (Statement of Accomplishment)
- Covers: JOINs, window functions, CTEs, subqueries, aggregate functions

**Database Design:**
- Normalization theory (1NF, 2NF, 3NF)
- Star schema for analytics
- Foreign key constraints

---

## ✍️ Author

**Jem Herbert-Rice**

Transitioning from Operations Manager to ML Engineer with focus on reinforcement learning and AI systems. This project demonstrates SQL proficiency for data analyst roles as part of a 5-year roadmap to AI research engineering.

- **GitHub:** [@JemHRice](https://github.com/JemHRice)
- **LinkedIn:** [jemhrice](https://linkedin.com/in/jemhrice)
- **Portfolio:** [House Price Predictor](https://house-price-predictor-7ge62jlm4m3awhc4py5cz8.streamlit.app/)

---

## 🙏 Acknowledgments

- **Dataset:** Kaggle E-Commerce Transactions
- **SQL Training:** DataCamp SQL Fundamentals Track
- **Database Design:** PostgreSQL Documentation
- **Inspiration:** Real-world e-commerce analytics challenges

---

**Last Updated:** February 2026  
**Project Status:** Complete - Ready for Production  
**Lines of SQL:** 500+ across 17 analytical queries  
**Business Insights:** 6 critical issues identified with actionable recommendations