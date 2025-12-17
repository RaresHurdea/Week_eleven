import os
import time
from app.exceptions import (
    PenguinDataException, FileNotLoadedException, InvalidSortOrderException
)
from app.services.data_ops import DataOperations
from app.ui import display, fun, image_to_ascii


class CommandHandler:
    def __init__(self, file_ops, visualizer, sorting_algorithms):
        self.file_ops = file_ops
        self.visualizer = visualizer
        self.sorting_algorithms = sorting_algorithms
        self.current_data = []
        self.current_filename = None
        self.default_sort = 'merge'
        self.image_path="900.jpeg"

    def list_files(self):
        files = self.file_ops.list_csv_files()
        if files:
            print("\nAvailable CSV files:")
            for f in files:
                print(f"  - {f}")
        else:
            print("No CSV files found in the data directory.")

    def load_file(self, filename: str):
        # Intelligent redirect to cleaned data if user asks for raw
        if filename == 'penguins.csv':
            clean_filename = 'penguins_data.csv'
            clean_filepath = os.path.join(self.file_ops.data_directory, clean_filename)

            if os.path.exists(clean_filepath):
                print(f"Notice: Loading preprocessed '{clean_filename}' instead of raw '{filename}'.")
                filename = clean_filename

        try:
            self.current_data = self.file_ops.load_csv(filename)
            self.current_filename = filename
            print(f"Loaded {len(self.current_data)} rows.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def filter_data(self, attribute: str, value: str):
        try:
            filtered = DataOperations.filter_data(self.current_data, attribute, value)
            print(f"Matches found: {len(filtered)}.")

            response = input("Do you want to save this data to a new file? (y/n) ").strip().lower()
            if response in ['y', 'yes']:
                filename = input("Please give the filename: ").strip()
                if not filename.endswith('.csv'):
                    filename += '.csv'
                self.file_ops.save_csv(filename, filtered)
                print(f"Saved to: {filename}")
            else:
                display.display_data_rows(filtered)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def describe_attribute(self, attribute: str):
        try:
            min_val, max_val, mean_val = DataOperations.describe_attribute(
                self.current_data, attribute
            )
            print(f"{attribute}: min = {min_val:.1f} max = {max_val:.1f} mean = {mean_val:.1f}")
        except PenguinDataException as e:
            print(f"Error: {e}")

    def unique_values(self, attribute: str):
        try:
            counts = DataOperations.unique_values(self.current_data, attribute)
            for value, count in sorted(counts.items()):
                print(f"{value}: {count} penguins")
        except PenguinDataException as e:
            print(f"Error: {e}")

    def sort_data(self, attribute: str, order: str):
        try:
            if not self.current_data:
                raise FileNotLoadedException("No data loaded.")

            if order not in ['asc', 'desc']:
                raise InvalidSortOrderException("Sort order must be 'asc' or 'desc'")

            algo_name, algo_func = self.sorting_algorithms[self.default_sort]

            start_time = time.time()
            sorted_data = algo_func(self.current_data, attribute, order == 'desc')
            execution_time = time.time() - start_time

            self.file_ops.log_sorting(len(self.current_data), algo_name, execution_time)

            print(f"Data sorted by {attribute} ({order}) using {algo_name}.")
            print(f"Execution time: {execution_time:.6f} seconds")

            display.display_data_rows(sorted_data)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def augment_data(self, percent: int, method: str):
        try:
            augmented = DataOperations.augment_data(self.current_data, percent, method)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"augmented_{method}_{percent}pct_{timestamp}.csv"

            self.file_ops.save_csv(filename, augmented)
            print(f"Dataset augmented and saved to: {filename}")
            print(f"New size: {len(augmented)} rows")

        except PenguinDataException as e:
            print(f"Error: {e}")

    def create_scatter(self, attr1: str, attr2: str):
        try:
            if not self.current_data:
                raise FileNotLoadedException("No data loaded.")

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"scatter_{attr1}_{attr2}_{timestamp}.png"
            filepath = os.path.join(self.file_ops.data_directory, filename)

            self.visualizer.create_scatter(self.current_data, attr1, attr2, filepath)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def create_histogram(self, attribute: str, bins: int):
        try:
            if not self.current_data:
                raise FileNotLoadedException("No data loaded.")

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"hist_{attribute}_{bins}bins_{timestamp}.png"
            filepath = os.path.join(self.file_ops.data_directory, filename)

            self.visualizer.create_histogram(self.current_data, attribute, bins, filepath)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def create_boxplot(self, group_by: str, attribute: str):
        try:
            if not self.current_data:
                raise FileNotLoadedException("No data loaded.")

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"boxplot_{group_by}_{attribute}_{timestamp}.png"
            filepath = os.path.join(self.file_ops.data_directory, filename)

            self.visualizer.create_boxplot(self.current_data, group_by, attribute, filepath)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def random_fact(self):
        print(f"\n Penguin Fact: {fun.get_random_fact()}\n")

    def draw_penguin(self):
        fun.draw_ascii_penguin()

    def convert_image_to_ascii(self):
        converter = image_to_ascii.ImageToASCII(self.image_path)
        converter.generate_ascii()
