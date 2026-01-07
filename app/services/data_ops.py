import random
import itertools
from typing import List, Dict, Any, Tuple
from app.exceptions import (
    FileNotLoadedException, InvalidColumnException,
    NonNumericAttributeException, PenguinDataException
)


class DataOperations:
    """
    A service class responsible for performing operations on penguin data,
    including filtering, statistical analysis, augmentation, and complex
    grouping algorithms.
    """

    NUMERIC_COLUMNS = {
        'Flipper Length (mm)', 'Culmen Length (mm)', 'Culmen Depth (mm)', 'Body Mass (g)',
        'flipper_length_mm', 'culmen_length_mm', 'culmen_depth_mm', 'body_mass_g'
    }
    STRING_COLUMNS = {
        'Species', 'Island', 'Sex', 'species', 'island', 'sex'
    }

    @staticmethod
    def filter_data(data: List[Dict], attribute: str, value: str) -> List[Dict]:
        """
        Filters the dataset based on a specific attribute and value.

        Args:
            data (List[Dict]): The dataset to filter.
            attribute (str): The column name to filter by.
            value (str): The value to match (or threshold for numeric columns).

        Returns:
            List[Dict]: A list of dictionaries representing the filtered rows.

        Raises:
            FileNotLoadedException: If the data list is empty.
            InvalidColumnException: If the attribute does not exist in the data.
        """
        if not data:
            raise FileNotLoadedException("No data loaded. Please load a file first.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"The specified column '{attribute}' does not exist.")

        filtered = []
        if attribute in DataOperations.NUMERIC_COLUMNS:
            try:
                numeric_value = float(value)
                for row in data:
                    try:
                        if float(row[attribute]) > numeric_value:
                            filtered.append(row)
                    except (ValueError, KeyError):
                        continue
            except ValueError:
                # Fallback if user provides non-numeric filter for numeric col
                pass
        else:
            for row in data:
                if row.get(attribute) == value:
                    filtered.append(row)
        return filtered

    @staticmethod
    def describe_attribute(data: List[Dict], attribute: str) -> Tuple[float, float, float]:
        """
        Calculates basic statistics (min, max, mean) for a numeric attribute.

        Args:
            data (List[Dict]): The dataset.
            attribute (str): The numeric column to analyze.

        Returns:
            Tuple[float, float, float]: A tuple containing (min, max, mean).

        Raises:
            NonNumericAttributeException: If the attribute is not numeric.
            PenguinDataException: If no valid numeric values are found.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"Column '{attribute}' does not exist.")
        if attribute not in DataOperations.NUMERIC_COLUMNS:
            raise NonNumericAttributeException(f"'{attribute}' is not numeric.")

        values = []
        for row in data:
            try:
                values.append(float(row[attribute]))
            except (ValueError, KeyError):
                continue

        if not values:
            raise PenguinDataException(f"No valid numeric values found for '{attribute}'")

        return min(values), max(values), sum(values) / len(values)

    @staticmethod
    def unique_values(data: List[Dict], attribute: str) -> Dict[str, int]:
        """
        Counts the occurrences of unique values for a specific attribute.

        Args:
            data (List[Dict]): The dataset.
            attribute (str): The column to analyze.

        Returns:
            Dict[str, int]: A dictionary mapping unique values to their counts.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"Column '{attribute}' does not exist.")

        counts = {}
        for row in data:
            val = row.get(attribute, '')
            if val:
                counts[val] = counts.get(val, 0) + 1
        return counts

    @staticmethod
    def augment_data(data: List[Dict], percent: int, method: str) -> List[Dict]:
        """
        Artificially increases the size of the dataset.

        Args:
            data (List[Dict]): The original dataset.
            percent (int): The percentage by which to increase the data size.
            method (str): The method of augmentation ('duplicate' or 'create').

        Returns:
            List[Dict]: The augmented dataset.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")

        num_to_add = int(len(data) * percent / 100)
        new_data = data.copy()

        if method == 'duplicate':
            for _ in range(num_to_add):
                new_data.append(random.choice(data).copy())
        elif method == 'create':
            columns = list(data[0].keys())
            # Simple random generation based on existing data range
            for _ in range(num_to_add):
                new_row = {}
                for col in columns:
                    if col in DataOperations.NUMERIC_COLUMNS:
                        vals = [float(r[col]) for r in data if r.get(col)]
                        if vals:
                            new_row[col] = round(random.uniform(min(vals), max(vals)), 1)
                        else:
                            new_row[col] = 0
                    elif col in DataOperations.STRING_COLUMNS:
                        vals = [r[col] for r in data if r.get(col)]
                        new_row[col] = random.choice(vals) if vals else ''
                    else:
                        new_row[col] = ''
                new_data.append(new_row)
        return new_data

    @staticmethod
    def get_random_subset(data: List[Dict], k: int) -> List[Dict]:
        """
        Selects a random subset of k penguins from the dataset.

        Args:
            data (List[Dict]): The source dataset.
            k (int): The number of penguins to select.

        Returns:
            List[Dict]: A list containing k random penguin dictionaries.

        Raises:
            PenguinDataException: If k is larger than the dataset size.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if k > len(data):
            raise PenguinDataException(f"Cannot select {k} penguins from a dataset of size {len(data)}.")
        return random.sample(data, k)

    @staticmethod
    def generate_research_groups(data: List[Dict], k: int) -> List[List[Dict]]:
        """
        Generates all possible groups of size k that contain at least one penguin
        from each species found in the dataset.

        Args:
            data (List[Dict]): The dataset (must be <= 10 items).
            k (int): The size of the research groups (must be >= 3).

        Returns:
            List[List[Dict]]: A list of valid groups, where each group is a list of penguins.

        Raises:
            PenguinDataException: If dataset is too large, k is invalid, or species data is missing.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if len(data) > 10:
            raise PenguinDataException("Dataset too large. Please load a set with at most 10 penguins.")
        if k < 3:
            raise PenguinDataException("Group size k must be at least 3.")
        if k > len(data):
            raise PenguinDataException(f"Group size {k} cannot exceed dataset size {len(data)}.")

        # Identify all species present in the current dataset
        available_species = {row.get('species') for row in data if row.get('species')}
        # Fallback for Capitalized key if lowercase not found
        if not available_species:
            available_species = {row.get('Species') for row in data if row.get('Species')}

        if not available_species:
            raise PenguinDataException("No species data found in the dataset.")

        valid_groups = []

        # Generate all combinations of size k
        for group in itertools.combinations(data, k):
            group_species = {row.get('species') or row.get('Species') for row in group}
            # Check if all available species are represented in this group
            if available_species.issubset(group_species):
                valid_groups.append(list(group))

        return valid_groups

    @staticmethod
    def split_penguins(data: List[Dict], threshold: float) -> List[Tuple[List[Dict], List[Dict]]]:
        """
        Generates all possible ways to split the penguins into two groups such that:
        1. Each group has at least 2 penguins.
        2. The total body mass of each group does not exceed the threshold.

        Args:
            data (List[Dict]): The dataset (must be <= 10 items).
            threshold (float): The maximum allowed body mass sum for a group.

        Returns:
            List[Tuple[List[Dict], List[Dict]]]: A list of tuples, where each tuple contains (Group1, Group2).

        Raises:
            PenguinDataException: If the dataset is too large or too small.
        """
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if len(data) > 10:
            raise PenguinDataException("Dataset too large. Please load a set with at most 10 penguins.")
        if len(data) < 4:
            raise PenguinDataException("Dataset too small to split into two groups of at least 2 penguins.")

        results = []
        n = len(data)

        # Helper to calculate mass
        def get_mass(penguin):
            try:
                # Handle keys for both raw and processed data
                key = 'body_mass_g' if 'body_mass_g' in penguin else 'Body Mass (g)'
                return float(penguin.get(key, 0))
            except (ValueError, TypeError):
                return 0.0

        # Fix the first element to Group 1 to avoid duplicate partitions (e.g. {A, B} vs {B, A})
        first_penguin = data[0]
        other_penguins = data[1:]

        # Iterate through possible sizes for Group 1.
        # Group 1 must have at least 2 elements, so we pick at least 1 more from 'others'.
        # Group 2 must have at least 2 elements, so Group 1 can have at most N-2 elements.
        # Range of items to pick from 'others': 1 to (N-2) - 1 => 1 to N-3
        for num_pick in range(1, n - 2):
            for chosen_others in itertools.combinations(other_penguins, num_pick):
                group_1 = [first_penguin] + list(chosen_others)

                # Group 2 is everyone not in Group 1. Using object identity logic via list reconstruction
                # Note: This relies on data containing unique dict objects
                g1_ids = {id(p) for p in group_1}
                group_2 = [p for p in data if id(p) not in g1_ids]

                mass_1 = sum(get_mass(p) for p in group_1)
                mass_2 = sum(get_mass(p) for p in group_2)

                if mass_1 <= threshold and mass_2 <= threshold:
                    results.append((group_1, group_2))

        return results

    # --- Sorting Algorithms ---

    @staticmethod
    def _get_comparable_value(row: Dict, key: str) -> Any:
        """Helper method to safely extract and cast values for comparison."""
        value = row.get(key, '')
        if key in DataOperations.NUMERIC_COLUMNS:
            try:
                return float(value)
            except (ValueError, TypeError):
                return float('inf')
        return str(value)

    @staticmethod
    def bubble_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sorts data using the Bubble Sort algorithm."""
        result = data.copy()
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                val1 = DataOperations._get_comparable_value(result[j], key)
                val2 = DataOperations._get_comparable_value(result[j + 1], key)

                if reverse:
                    if val1 < val2:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
                else:
                    if val1 > val2:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
            if not swapped:
                break
        return result

    @staticmethod
    def merge_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sorts data using the Merge Sort algorithm (recursive)."""
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = DataOperations.merge_sort(data[:mid], key, reverse)
        right = DataOperations.merge_sort(data[mid:], key, reverse)
        return DataOperations._merge(left, right, key, reverse)

    @staticmethod
    def _merge(left, right, key, reverse):
        """Helper method for merge_sort to combine two sorted lists."""
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            l_val = DataOperations._get_comparable_value(left[i], key)
            r_val = DataOperations._get_comparable_value(right[j], key)

            condition = (l_val >= r_val) if reverse else (l_val <= r_val)
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def quick_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sorts data using the Quick Sort algorithm."""
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        pivot_val = DataOperations._get_comparable_value(pivot, key)

        left = []
        middle = []
        right = []

        for item in data:
            val = DataOperations._get_comparable_value(item, key)
            if val < pivot_val:
                left.append(item)
            elif val > pivot_val:
                right.append(item)
            else:
                middle.append(item)

        if reverse:
            return DataOperations.quick_sort(right, key, reverse) + middle + DataOperations.quick_sort(left, key,
                                                                                                       reverse)
        else:
            return DataOperations.quick_sort(left, key, reverse) + middle + DataOperations.quick_sort(right, key,
                                                                                                      reverse)

    @staticmethod
    def insertion_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sorts data using the Insertion Sort algorithm."""
        result = data.copy()
        for i in range(1, len(result)):
            key_item = result[i]
            key_val = DataOperations._get_comparable_value(key_item, key)
            j = i - 1
            while j >= 0:
                comp_val = DataOperations._get_comparable_value(result[j], key)
                condition = (comp_val < key_val) if reverse else (comp_val > key_val)

                if condition:
                    result[j + 1] = result[j]
                    j -= 1
                else:
                    break
            result[j + 1] = key_item
        return result

    @staticmethod
    def selection_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sorts data using the Selection Sort algorithm."""
        result = data.copy()
        for i in range(len(result)):
            extreme_idx = i
            extreme_val = DataOperations._get_comparable_value(result[i], key)

            for j in range(i + 1, len(result)):
                curr_val = DataOperations._get_comparable_value(result[j], key)
                condition = (curr_val > extreme_val) if reverse else (curr_val < extreme_val)

                if condition:
                    extreme_idx = j
                    extreme_val = curr_val

            result[i], result[extreme_idx] = result[extreme_idx], result[i]
        return result