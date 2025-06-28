# scripts/migrate.py

import sys
import os

# Add the root of the project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import init_db

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized with tables and constraints.")
