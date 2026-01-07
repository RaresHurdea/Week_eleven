import os
import time
from app.exceptions import (
    PenguinDataException, FileNotLoadedException, InvalidSortOrderException
)
from app.services.data_ops import DataOperations
from app.ui import display, fun, image_to_ascii


class CommandHandler:
    """
    Handles specific user commands by coordinating between the User Interface
    and the Data Operations service.
    """

    def __init__(self, file_ops, visualizer, sorting_algorithms):
        self.file_ops = file_ops
        self.visualizer = visualizer
        self.sorting_algorithms = sorting_algorithms
        self.current_data = []
        self.current_filename = None
        self.default_sort = 'merge'
        self.image_path = "900.jpeg"

    def list_files(self):
        """Displays a list of available CSV files in the data directory."""
        files = self.file_ops.list_csv_files()
        if files:
            print("\nAvailable CSV files:")
            for f in files:
                print(f"  - {f}")
        else:
            print("No CSV files found in the data directory.")

    def load_file(self, filename: str):
        """
        Loads the specified CSV file into memory.

        Args:
            filename (str): The name of the file to load.
        """
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
        """
        Filters the currently loaded data and offers to save the result.

        Args:
            attribute (str): The column to filter by.
            value (str): The value to match.
        """
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
        """
        Prints descriptive statistics for a numeric attribute.

        Args:
            attribute (str): The numeric attribute to describe.
        """
        try:
            min_val, max_val, mean_val = DataOperations.describe_attribute(
                self.current_data, attribute
            )
            print(f"{attribute}: min = {min_val:.1f} max = {max_val:.1f} mean = {mean_val:.1f}")
        except PenguinDataException as e:
            print(f"Error: {e}")

    def unique_values(self, attribute: str):
        """
        Prints unique values and their counts for an attribute.

        Args:
            attribute (str): The attribute to analyze.
        """
        try:
            counts = DataOperations.unique_values(self.current_data, attribute)
            for value, count in sorted(counts.items()):
                print(f"{value}: {count} penguins")
        except PenguinDataException as e:
            print(f"Error: {e}")

    def sort_data(self, attribute: str, order: str):
        """
        Sorts the data and displays the result.

        Args:
            attribute (str): The column to sort by.
            order (str): 'asc' for ascending, 'desc' for descending.
        """
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
        """
        Augments the dataset and saves the result to a new file.

        Args:
            percent (int): Percentage to increase size by.
            method (str): 'duplicate' or 'create'.
        """
        try:
            augmented = DataOperations.augment_data(self.current_data, percent, method)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"augmented_{method}_{percent}pct_{timestamp}.csv"

            self.file_ops.save_csv(filename, augmented)
            print(f"Dataset augmented and saved to: {filename}")
            print(f"New size: {len(augmented)} rows")

        except PenguinDataException as e:
            print(f"Error: {e}")

    def save_random(self, k: int, filename: str):
        """
        Saves a random subset of k penguins to a file.

        Args:
            k (int): Number of penguins to select.
            filename (str): The destination filename.
        """
        try:
            subset = DataOperations.get_random_subset(self.current_data, k)

            if not filename.endswith('.csv'):
                filename += '.csv'

            self.file_ops.save_csv(filename, subset)
            print(f"Successfully saved {k} random penguins to {filename}.")
        except PenguinDataException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def generate_research_groups(self, k: int):
        """
        Finds and displays research groups satisfying the diversity criteria.

        Args:
            k (int): The size of the research groups.
        """
        try:
            groups = DataOperations.generate_research_groups(self.current_data, k)

            if not groups:
                print("Error: No research groups satisfying the criteria could be generated.")
                return

            print(f"\nFound {len(groups)} possible research groups of size {k}:\n")
            for i, group in enumerate(groups, 1):
                print(f"Group {i}:")
                for p in group:
                    # Print simplified info: species and ID if available, or just index
                    info = f"{p.get('species') or p.get('Species')}"
                    if 'Individual ID' in p:
                        info += f" (ID: {p['Individual ID']})"
                    print(f"  - {info}")
                print("-" * 20)

        except PenguinDataException as e:
            print(f"Error: {e}")

    def split_into_groups(self, threshold: float):
        """
        Splits the penguins into two groups based on mass threshold.

        Args:
            threshold (float): Maximum allowed mass for a group.
        """
        try:
            splits = DataOperations.split_penguins(self.current_data, threshold)

            if not splits:
                print(f"Error: No valid splits found where both groups have mass <= {threshold}.")
                return

            print(f"\nFound {len(splits)} valid ways to split the penguins:\n")
            for i, (g1, g2) in enumerate(splits, 1):
                mass1 = sum(float(p.get('body_mass_g', p.get('Body Mass (g)', 0))) for p in g1)
                mass2 = sum(float(p.get('body_mass_g', p.get('Body Mass (g)', 0))) for p in g2)

                print(f"Split {i}:")
                print(f"  Group A: {len(g1)} penguins, Total Mass: {mass1:.1f}")
                print(f"  Group B: {len(g2)} penguins, Total Mass: {mass2:.1f}")
                print("-" * 20)

        except PenguinDataException as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Invalid threshold value.")

    def create_scatter(self, attr1: str, attr2: str):
        """Generates a scatter plot for two attributes."""
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
        """Generates a histogram for a specific attribute."""
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
        """Generates a boxplot grouping data by an attribute."""
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
        """Displays a random penguin fact."""
        print(f"\n Penguin Fact: {fun.get_random_fact()}\n")

    def draw_penguin(self):
        """Draws an ASCII penguin."""
        fun.draw_ascii_penguin()

    def convert_image_to_ascii(self):
        """Converts an image to ASCII art."""
        converter = image_to_ascii.ImageToASCII(self.image_path)
        converter.generate_ascii()