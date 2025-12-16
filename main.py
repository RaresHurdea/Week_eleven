import sys
import os

# Ensure the current directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ui.analyzer import PenguinAnalyzer
from app.services.cleaning import analyze_missing_data, preprocess_penguins_data

if __name__ == "__main__":
    print("Initializing Penguin Data Analysis...")

    # Ensure data directory exists
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Check if we need to preprocess data
    # Logic: If raw exists but clean doesn't, or if clean is missing
    raw_path = os.path.join(data_dir, 'penguins.csv')
    clean_path = os.path.join(data_dir, 'penguins_data.csv')

    if os.path.exists(raw_path) and not os.path.exists(clean_path):
        print("Preprocessing data...")
        analyze_missing_data(data_dir=data_dir)
        preprocess_penguins_data(data_dir=data_dir)

    # Start Application
    analyzer = PenguinAnalyzer(data_directory=data_dir)
    analyzer.run()