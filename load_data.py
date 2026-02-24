import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "ecommerce"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def load_csv_data():
    """Load data from CSV"""
    print("Loading CSV data...")
    df = pd.read_csv("data/ecommerce_data.csv")
    print(f"Loaded {len(df)} rows")
    return df


def schema_exists(conn):
    """Check if customers table already exists"""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'customers'
            );
        """
        )
        return cur.fetchone()[0]


def create_schema(conn):
    """Execute schema.sql to create tables if they don't exist"""
    if schema_exists(conn):
        print("Schema already exists, skipping creation...")
        return

    print("Creating database schema...")
    import sys

    sys.stdout.flush()

    with open("schema.sql", "r") as f:
        schema = f.read()

    # Split by semicolon and execute each statement individually
    statements = [stmt.strip() for stmt in schema.split(";") if stmt.strip()]

    with conn.cursor() as cur:
        for i, stmt in enumerate(statements):
            print(
                f"  Executing statement {i+1}/{len(statements)}...", end="", flush=True
            )
            sys.stdout.flush()
            cur.execute(stmt)
            print(" ✓")
            sys.stdout.flush()

    conn.commit()
    print("Schema created successfully")
    sys.stdout.flush()


def insert_customers(df, conn):
    """Insert unique customers"""
    print("Inserting customers...")
    customers = df[
        ["customer_id", "customer_age", "customer_gender", "region"]
    ].drop_duplicates()

    values = [
        (row["customer_id"], row["customer_age"], row["customer_gender"], row["region"])
        for _, row in customers.iterrows()
    ]

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO customers (customer_id, customer_age, customer_gender, region)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """,
            values,
        )

    conn.commit()
    print(f"Inserted {len(customers)} customers")


def insert_products(df, conn):
    """Insert unique products"""
    print("Inserting products...")
    products = df[["product_id", "category", "price"]].drop_duplicates()

    values = [
        (row["product_id"], row["category"], row["price"])
        for _, row in products.iterrows()
    ]

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO products (product_id, category, price)
            VALUES (%s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING
        """,
            values,
        )

    conn.commit()
    print(f"Inserted {len(products)} products")


def insert_orders(df, conn):
    """Insert orders"""
    print("Inserting orders...")
    orders = df[
        [
            "order_id",
            "customer_id",
            "order_date",
            "payment_method",
            "shipping_cost",
            "delivery_time_days",
        ]
    ].drop_duplicates()

    values = [
        (
            row["order_id"],
            row["customer_id"],
            row["order_date"],
            row["payment_method"],
            row["shipping_cost"],
            row["delivery_time_days"],
        )
        for _, row in orders.iterrows()
    ]

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO orders (order_id, customer_id, order_date, payment_method, 
                               shipping_cost, delivery_time_days)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING
        """,
            values,
        )

    conn.commit()
    print(f"Inserted {len(orders)} orders")


def insert_order_items(df, conn):
    """Insert order items"""
    print("Inserting order items...")
    items = df[
        [
            "order_id",
            "product_id",
            "quantity",
            "discount",
            "total_amount",
            "profit_margin",
            "returned",
        ]
    ]

    values = [
        (
            row["order_id"],
            row["product_id"],
            row["quantity"],
            row["discount"],
            row["total_amount"],
            row["profit_margin"],
            row["returned"],
        )
        for _, row in items.iterrows()
    ]

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO order_items (order_id, product_id, quantity, discount, 
                                    total_amount, profit_margin, returned)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id, product_id) DO NOTHING
        """,
            values,
        )

    conn.commit()
    print(f"Inserted {len(items)} order items")


def main():
    """Main execution"""
    # Load CSV
    df = load_csv_data()

    # Connect to database
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(**DB_PARAMS)

    try:
        # Create schema
        create_schema(conn)

        # Insert data
        insert_customers(df, conn)
        insert_products(df, conn)
        insert_orders(df, conn)
        insert_order_items(df, conn)

        print("\n✓ Data loaded successfully!")

        # Show counts
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM customers")
            print(f"Customers: {cur.fetchone()[0]}")

            cur.execute("SELECT COUNT(*) FROM products")
            print(f"Products: {cur.fetchone()[0]}")

            cur.execute("SELECT COUNT(*) FROM orders")
            print(f"Orders: {cur.fetchone()[0]}")

            cur.execute("SELECT COUNT(*) FROM order_items")
            print(f"Order Items: {cur.fetchone()[0]}")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
