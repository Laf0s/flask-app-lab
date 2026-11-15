"""Insert data into products table

Revision ID: 733ff9fb286a
Revises: 2e360a8861d1
Create Date: 2026-11-15 20:38:37.220086

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column



# revision identifiers, used by Alembic.
revision = '733ff9fb286a'
down_revision = '2e360a8861d1'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String)
    )
    products_table = sa.table(
        "products",
        sa.column("name", sa.String),
        sa.column("price", sa.Float),
        sa.column("active", sa.Boolean),
        sa.column("category_id", sa.Integer),
    )

    op.bulk_insert(categories_table, [
        {"name": "Electronics"},
        {"name": "Books"},
        {"name": "Clothing"},
    ])

    op.bulk_insert(products_table, [
        {"name": "Laptop", "price": 1200.0, "active": True, "category_id": 2},
        {"name": "Smartphone", "price": 800.0, "active": True, "category_id": 2},
        {"name": "Novel", "price": 20.0, "active": True, "category_id": 3},
        {"name": "T-Shirt", "price": 25.0, "active": False, "category_id": 4},
    ])


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)