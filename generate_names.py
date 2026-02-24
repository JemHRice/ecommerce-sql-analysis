import pandas as pd
import psycopg2
from faker import Faker
import random

# Database connection
DB_PARAMS = {
    "dbname": "ecommerce",
    "user": "postgres",
    "password": "YumSpagh3tti!",
    "host": "localhost",
    "port": "5432",
}

fake = Faker()


def generate_customer_names():
    """Generate names for existing customers"""
    conn = psycopg2.connect(**DB_PARAMS)

    # Get all customers
    customers = pd.read_sql(
        "SELECT customer_id, customer_age, customer_gender FROM customers", conn
    )

    print(f"Generating names for {len(customers)} customers...")

    names = []
    for _, row in customers.iterrows():
        gender = row["customer_gender"].lower()

        # Generate name based on gender
        if gender == "male":
            name = fake.name_male()
        elif gender == "female":
            name = fake.name_female()
        else:
            name = fake.name()

        names.append({"customer_id": row["customer_id"], "customer_name": name})

    # Update database
    cursor = conn.cursor()

    # Add column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN customer_name VARCHAR(100)")
        conn.commit()
        print("Added customer_name column")
    except:
        conn.rollback()
        print("customer_name column already exists")

    # Update names
    for entry in names:
        cursor.execute(
            "UPDATE customers SET customer_name = %s WHERE customer_id = %s",
            (entry["customer_name"], entry["customer_id"]),
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✓ Updated {len(names)} customer names")


if __name__ == "__main__":
    generate_customer_names()


def generate_product_names():
    """Generate product names based on category"""
    conn = psycopg2.connect(**DB_PARAMS)

    # Get all products
    products = pd.read_sql("SELECT product_id, category, price FROM products", conn)

    print(f"Generating names for {len(products)} products...")

    # Product name templates by category
    templates = {
        "Electronics": ["Smart", "Pro", "Ultra", "Max", "Elite", "Premium", "Digital"],
        "Fashion": ["Classic", "Trendy", "Vintage", "Modern", "Elegant", "Casual"],
        "Home": ["Comfort", "Deluxe", "Essential", "Premium", "Standard", "Elite"],
        "Beauty": ["Radiance", "Glow", "Pure", "Natural", "Luxury", "Essential"],
        "Sports": ["Active", "Pro", "Performance", "Training", "Elite", "Outdoor"],
        "Toys": ["Fun", "Classic", "Adventure", "Creative", "Educational", "Play"],
        "Grocery": ["Fresh", "Organic", "Premium", "Natural", "Wholesome", "Daily"],
    }

    category_items = {
        "Electronics": [
            "Phone",
            "Laptop",
            "Tablet",
            "Headphones",
            "Speaker",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Camera",
            "Smartwatch",
        ],
        "Fashion": [
            "Shirt",
            "Jeans",
            "Dress",
            "Jacket",
            "Shoes",
            "Bag",
            "Watch",
            "Sunglasses",
            "Scarf",
            "Belt",
        ],
        "Home": [
            "Sofa",
            "Table",
            "Chair",
            "Lamp",
            "Rug",
            "Curtain",
            "Pillow",
            "Blanket",
            "Mirror",
            "Shelf",
        ],
        "Beauty": [
            "Cream",
            "Serum",
            "Moisturizer",
            "Cleanser",
            "Mask",
            "Lipstick",
            "Foundation",
            "Perfume",
            "Shampoo",
            "Conditioner",
        ],
        "Sports": [
            "Shoes",
            "Ball",
            "Racket",
            "Weights",
            "Mat",
            "Bottle",
            "Gloves",
            "Shorts",
            "Jersey",
            "Gear",
        ],
        "Toys": [
            "Puzzle",
            "Blocks",
            "Doll",
            "Car",
            "Game",
            "Robot",
            "Bear",
            "Ball",
            "Kit",
            "Set",
        ],
        "Grocery": [
            "Bread",
            "Milk",
            "Eggs",
            "Cheese",
            "Coffee",
            "Tea",
            "Rice",
            "Pasta",
            "Oil",
            "Juice",
        ],
    }

    names = []
    for _, row in products.iterrows():
        category = row["category"]
        price = row["price"]

        # Generate name based on category
        prefix = random.choice(templates.get(category, ["Premium"]))
        item = random.choice(category_items.get(category, ["Item"]))

        # Add quality indicator based on price
        if price > 500:
            quality = "Platinum"
        elif price > 200:
            quality = "Gold"
        elif price > 100:
            quality = "Silver"
        else:
            quality = ""

        # Construct name
        if quality:
            product_name = f"{prefix} {item} {quality} Edition"
        else:
            product_name = f"{prefix} {item}"

        names.append({"product_id": row["product_id"], "product_name": product_name})

    # Update database
    cursor = conn.cursor()

    # Add column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN product_name VARCHAR(150)")
        conn.commit()
        print("Added product_name column")
    except:
        conn.rollback()
        print("product_name column already exists")

    # Update names
    for entry in names:
        cursor.execute(
            "UPDATE products SET product_name = %s WHERE product_id = %s",
            (entry["product_name"], entry["product_id"]),
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✓ Updated {len(names)} product names")


if __name__ == "__main__":
    generate_customer_names()
    generate_product_names()
